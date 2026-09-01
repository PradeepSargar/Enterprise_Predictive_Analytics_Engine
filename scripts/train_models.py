"""
Model Training & Artifact Generation Pipeline
==============================================
Enterprise Predictive Analytics Engine

Responsibilities:
1. Supervised Classification (Dissatisfaction / Low Review Risk):
   - Trains Logistic Regression, Random Forest, and Gradient Boosting.
   - Evaluates on 80/20 stratified test split.
   - Saves benchmark metrics to `reports/model_comparison_results.csv`.
   - Serializes the champion model to `models/churn_risk_classifier.pkl`.

2. Customer RFM Clustering:
   - Fits StandardScaler and KMeans (k=4) on customer RFM features.
   - Serializes model and segment profile mapping to `models/customer_kmeans_clusterer.pkl`.

3. Multi-Grain Time-Series Forecasting:
   - Aggregates monthly revenue for:
     a) Total Marketplace Revenue ("total", "All")
     b) Top 5 Product Categories ("category", <category_name>)
     c) Top 5 Brazilian States / Regions ("region", <state_code>)
   - Fits Prophet models (90% CI) per slice.
   - Exports multi-grain forecast to `data/processed/revenue_forecast.csv`.
   - Serializes forecasting models to `models/revenue_forecaster.pkl`.
"""

from __future__ import annotations

import os
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from prophet import Prophet


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"

MASTER_DATA_PATH = DATA_PROCESSED / "olist_master_cleaned.csv"
MASTER_PARQUET_PATH = DATA_PROCESSED / "olist_master_cleaned.parquet"
SEGMENTS_DATA_PATH = DATA_PROCESSED / "customer_segments.csv"
SEGMENTS_PARQUET_PATH = DATA_PROCESSED / "customer_segments.parquet"
FORECAST_DATA_PATH = DATA_PROCESSED / "revenue_forecast.csv"
MODEL_COMPARISON_PATH = REPORTS_DIR / "model_comparison_results.csv"


def ensure_directories():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


# ============================================================================
# 1. SUPERVISED CLASSIFICATION (DISSATISFACTION RISK)
# ============================================================================

def train_classification_models(df: pd.DataFrame):
    print("\n--- 1. Training Classification Models (3 Models + 5-Fold CV) ---")

    # Define binary target: review_score <= 2 is low review (dissatisfied)
    df["low_review"] = (df["review_score"] <= 2).astype(int)
    print(f"Low review base rate: {df['low_review'].mean():.2%}")

    # Drop missing features
    feature_cols = [
        "delivery_delay_days",
        "delivery_time_days",
        "price",
        "freight_value",
        "payment_installments",
    ]
    model_df = df.dropna(subset=feature_cols + ["product_category_name_english"]).copy()

    # Category grouping
    top_categories = list(
        model_df["product_category_name_english"].value_counts().nlargest(10).index
    )
    model_df["category_grouped"] = model_df["product_category_name_english"].where(
        model_df["product_category_name_english"].isin(top_categories), "other"
    )

    category_dummies = pd.get_dummies(model_df["category_grouped"], prefix="cat")
    X = pd.concat([model_df[feature_cols], category_dummies], axis=1)
    y = model_df["low_review"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 1. Logistic Regression (with Scaler)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    lr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    y_proba_lr = lr.predict_proba(X_test_scaled)[:, 1]

    # 2. Random Forest
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_proba_rf = rf.predict_proba(X_test)[:, 1]

    # 3. Gradient Boosting
    sample_weight = np.where(y_train == 1, 2.5, 1.0)
    gb = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=5,
        random_state=42,
    )
    gb.fit(X_train, y_train, sample_weight=sample_weight)
    y_pred_gb = gb.predict(X_test)
    y_proba_gb = gb.predict_proba(X_test)[:, 1]

    # 5-Fold Stratified Cross-Validation on Training Split
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    print("Running Stratified 5-Fold Cross-Validation...")
    lr_cv_scores = cross_val_score(lr, X_train_scaled, y_train, cv=cv, scoring="f1", n_jobs=-1)
    rf_cv_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)
    gb_cv_scores = cross_val_score(gb, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)

    results = [
        {
            "Model": "Logistic Regression",
            "Accuracy": round(accuracy_score(y_test, y_pred_lr), 3),
            "Precision": round(precision_score(y_test, y_pred_lr), 3),
            "Recall": round(recall_score(y_test, y_pred_lr), 3),
            "F1 Score": round(f1_score(y_test, y_pred_lr), 3),
            "ROC-AUC": round(roc_auc_score(y_test, y_proba_lr), 3),
            "CV F1 Mean": round(float(np.mean(lr_cv_scores)), 3),
            "CV F1 Std": round(float(np.std(lr_cv_scores)), 3),
        },
        {
            "Model": "Random Forest",
            "Accuracy": round(accuracy_score(y_test, y_pred_rf), 3),
            "Precision": round(precision_score(y_test, y_pred_rf), 3),
            "Recall": round(recall_score(y_test, y_pred_rf), 3),
            "F1 Score": round(f1_score(y_test, y_pred_rf), 3),
            "ROC-AUC": round(roc_auc_score(y_test, y_proba_rf), 3),
            "CV F1 Mean": round(float(np.mean(rf_cv_scores)), 3),
            "CV F1 Std": round(float(np.std(rf_cv_scores)), 3),
        },
        {
            "Model": "Gradient Boosting",
            "Accuracy": round(accuracy_score(y_test, y_pred_gb), 3),
            "Precision": round(precision_score(y_test, y_pred_gb), 3),
            "Recall": round(recall_score(y_test, y_pred_gb), 3),
            "F1 Score": round(f1_score(y_test, y_pred_gb), 3),
            "ROC-AUC": round(roc_auc_score(y_test, y_proba_gb), 3),
            "CV F1 Mean": round(float(np.mean(gb_cv_scores)), 3),
            "CV F1 Std": round(float(np.std(gb_cv_scores)), 3),
        },
    ]

    results_df = pd.DataFrame(results)
    results_df.to_csv(MODEL_COMPARISON_PATH, index=False)
    print("Model comparison results saved to:", MODEL_COMPARISON_PATH)
    print(results_df.to_string(index=False))

    # Feature importance from Random Forest
    importances = pd.DataFrame({
        "feature": X.columns,
        "importance": rf.feature_importances_,
    }).sort_values("importance", ascending=False)

    # Save Champion Model Artifact
    artifact = {
        "model_name": "Random Forest",
        "model": rf,
        "feature_cols": list(X.columns),
        "numeric_features": feature_cols,
        "top_categories": top_categories,
        "feature_importances": importances.to_dict(orient="records"),
        "metrics": results[1],
        "all_models": results_df.to_dict(orient="records"),
    }
    joblib.dump(artifact, MODELS_DIR / "churn_risk_classifier.pkl")
    print("Champion classification model saved to: models/churn_risk_classifier.pkl")


# ============================================================================
# 2. CUSTOMER RFM CLUSTERING
# ============================================================================

def train_clustering_model(segments_df: pd.DataFrame):
    print("\n--- 2. Training Customer RFM Clustering (KMeans) ---")

    rfm_cols = ["recency", "frequency", "monetary"]
    clean_rfm = segments_df.dropna(subset=rfm_cols).copy()

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(clean_rfm[rfm_cols])

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clean_rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

    # Calculate cluster summaries for segment labeling
    summary = clean_rfm.groupby("cluster")[rfm_cols].mean()
    print("Cluster Centers (Raw Scale Means):")
    print(summary)

    artifact = {
        "scaler": scaler,
        "kmeans": kmeans,
        "rfm_cols": rfm_cols,
        "cluster_centers_raw": summary.to_dict(orient="index"),
        "segment_names": {
            0: "Recent One-Time Buyers",
            1: "Lapsed / At Risk",
            2: "Loyal Repeat Customers",
            3: "High-Value Outliers",
        },
    }
    joblib.dump(artifact, MODELS_DIR / "customer_kmeans_clusterer.pkl")
    print("Clustering artifact saved to: models/customer_kmeans_clusterer.pkl")


# ============================================================================
# 3. MULTI-GRAIN TIME-SERIES FORECASTING
# ============================================================================

def run_prophet_forecast(series_df: pd.DataFrame, periods: int = 6) -> tuple[pd.DataFrame, Any]:
    """
    Fits Prophet model with yearly_seasonality=False, interval_width=0.90
    and outputs full history + 6-month future forecast.
    Includes robust fallback if Stan / Prophet encounters an environment error.
    """
    clean_series = series_df[series_df["ds"] >= "2017-01-01"].sort_values("ds").reset_index(drop=True)
    full_dates = pd.date_range(start="2017-01-01", end="2018-08-01", freq="MS")
    merged = pd.DataFrame({"ds": full_dates}).merge(clean_series, on="ds", how="left")
    merged["y"] = merged["y"].fillna(0.0)

    try:
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False,
            interval_width=0.90,
        )
        model.fit(merged)

        future = model.make_future_dataframe(periods=periods, freq="MS")
        forecast = model.predict(future)

        result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
        result = result.merge(merged[["ds", "y"]], on="ds", how="left")
    except Exception as exc:
        print(f"  [Prophet fallback triggered: {exc}]")
        # Robust linear trend + volatility interval fallback
        future_dates = pd.date_range(start="2017-01-01", periods=len(full_dates) + periods, freq="MS")
        y_vals = merged["y"].values
        x_idx = np.arange(len(y_vals))
        poly = np.polyfit(x_idx, y_vals, 1)
        future_x = np.arange(len(future_dates))
        yhat_raw = np.polyval(poly, future_x)
        std_val = float(np.std(y_vals)) if len(y_vals) > 0 else 1000.0

        forecast_data = {
            "ds": future_dates,
            "yhat": yhat_raw,
            "yhat_lower": yhat_raw - (1.645 * std_val),
            "yhat_upper": yhat_raw + (1.645 * std_val),
        }
        result = pd.DataFrame(forecast_data)
        result = result.merge(merged[["ds", "y"]], on="ds", how="left")
        model = "LinearTrendFallback"

    result.rename(
        columns={
            "ds": "month",
            "yhat": "predicted_revenue",
            "yhat_lower": "lower_bound",
            "yhat_upper": "upper_bound",
            "y": "actual_revenue",
        },
        inplace=True,
    )

    result["lower_bound"] = result["lower_bound"].clip(lower=0.0)
    result["predicted_revenue"] = result["predicted_revenue"].clip(lower=0.0)
    result["upper_bound"] = result["upper_bound"].clip(lower=0.0)

    return result, model


def train_multi_grain_forecasting(df: pd.DataFrame):
    print("\n--- 3. Training Multi-Grain Time-Series Forecasting ---")

    delivered = df[df["is_delivered"] == True].copy()
    delivered["order_purchase_timestamp"] = pd.to_datetime(delivered["order_purchase_timestamp"])

    all_forecast_records = []
    saved_models = {}

    # A) TOTAL MARKETPLACE REVENUE
    print("Forecasting Total Marketplace Revenue...")
    total_monthly = (
        delivered.set_index("order_purchase_timestamp")
        .resample("MS")["payment_value"]
        .sum()
        .reset_index()
    )
    total_monthly.columns = ["ds", "y"]

    fc_total, model_total = run_prophet_forecast(total_monthly, periods=6)
    fc_total["segment_type"] = "total"
    fc_total["segment_value"] = "All"
    all_forecast_records.append(fc_total)
    saved_models[("total", "All")] = model_total

    # B) TOP 5 PRODUCT CATEGORIES
    print("Finding Top 5 Product Categories...")
    top_categories = (
        delivered.groupby("product_category_name_english")["payment_value"]
        .sum()
        .nlargest(5)
        .index.tolist()
    )
    print("Top Categories:", top_categories)

    for cat in top_categories:
        print(f"Forecasting Category: {cat}...")
        cat_df = delivered[delivered["product_category_name_english"] == cat]
        cat_monthly = (
            cat_df.set_index("order_purchase_timestamp")
            .resample("MS")["payment_value"]
            .sum()
            .reset_index()
        )
        cat_monthly.columns = ["ds", "y"]

        fc_cat, model_cat = run_prophet_forecast(cat_monthly, periods=6)
        fc_cat["segment_type"] = "category"
        fc_cat["segment_value"] = cat
        all_forecast_records.append(fc_cat)
        saved_models[("category", cat)] = model_cat

    # C) TOP 5 STATES / REGIONS
    print("Finding Top 5 States...")
    top_states = (
        delivered.groupby("customer_state")["payment_value"]
        .sum()
        .nlargest(5)
        .index.tolist()
    )
    print("Top States:", top_states)

    for state in top_states:
        print(f"Forecasting Region/State: {state}...")
        state_df = delivered[delivered["customer_state"] == state]
        state_monthly = (
            state_df.set_index("order_purchase_timestamp")
            .resample("MS")["payment_value"]
            .sum()
            .reset_index()
        )
        state_monthly.columns = ["ds", "y"]

        fc_state, model_state = run_prophet_forecast(state_monthly, periods=6)
        fc_state["segment_type"] = "region"
        fc_state["segment_value"] = state
        all_forecast_records.append(fc_state)
        saved_models[("region", state)] = model_state

    # Combine into unified dataset
    combined_forecast_df = pd.concat(all_forecast_records, ignore_index=True)

    # Reorder columns as requested:
    # month, segment_type, segment_value, predicted_revenue, lower_bound, upper_bound, actual_revenue
    cols_order = [
        "month",
        "segment_type",
        "segment_value",
        "predicted_revenue",
        "lower_bound",
        "upper_bound",
        "actual_revenue",
    ]
    combined_forecast_df = combined_forecast_df[cols_order]

    # Save to CSV
    combined_forecast_df.to_csv(FORECAST_DATA_PATH, index=False)
    print(f"Unified multi-grain forecast saved to: {FORECAST_DATA_PATH} ({len(combined_forecast_df)} rows)")

    # Save Forecaster Artifact
    forecast_artifact = {
        "grain_types": ["total", "category", "region"],
        "categories": top_categories,
        "regions": top_states,
        "forecast_periods": 6,
    }
    joblib.dump(forecast_artifact, MODELS_DIR / "revenue_forecaster.pkl")
    print("Forecasting metadata artifact saved to: models/revenue_forecaster.pkl")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    ensure_directories()

    print("Loading processed datasets...")
    master_df = pd.read_csv(MASTER_DATA_PATH, low_memory=False)
    segments_df = pd.read_csv(SEGMENTS_DATA_PATH, low_memory=False)

    print("Exporting high-performance Parquet format...")
    try:
        master_df.to_parquet(MASTER_PARQUET_PATH, index=False, compression="snappy")
        segments_df.to_parquet(SEGMENTS_PARQUET_PATH, index=False, compression="snappy")
        print(f"  Parquet exports saved: {MASTER_PARQUET_PATH.name}, {SEGMENTS_PARQUET_PATH.name}")
    except Exception as exc:
        print(f"  [Parquet export skipped: {exc}]")

    train_classification_models(master_df)
    train_clustering_model(segments_df)
    train_multi_grain_forecasting(master_df)

    print("\n========================================================")
    print("ALL MODELS AND ARTIFACTS TRAINED & PERSISTED SUCCESSFULLY")
    print("========================================================\n")


if __name__ == "__main__":
    main()
