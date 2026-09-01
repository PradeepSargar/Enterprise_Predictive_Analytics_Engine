"""
Centralized data & model loading layer for the Enterprise Analytics Engine.

Responsibilities:
- Locating project data files and serialized ML models safely
- Loading processed datasets (master data, RFM segments, multi-grain forecasts)
- Parsing date columns and validating schema integrity
- Loading pickled ML models (classification champion, KMeans clusterer, forecaster)
- Providing interactive risk prediction utility
- Caching datasets for high-performance dashboard rendering

Pages must import data and model loading functions from this module
instead of reading CSVs or pickle files directly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# =====================================================================
# PROJECT PATHS
# =====================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"


# =====================================================================
# DATA & MODEL FILE PATHS
# =====================================================================

MASTER_DATA_PATH = PROCESSED_DATA_DIR / "olist_master_cleaned.csv"
MASTER_PARQUET_PATH = PROCESSED_DATA_DIR / "olist_master_cleaned.parquet"
CUSTOMER_SEGMENTS_PATH = PROCESSED_DATA_DIR / "customer_segments.csv"
CUSTOMER_SEGMENTS_PARQUET_PATH = PROCESSED_DATA_DIR / "customer_segments.parquet"
REVENUE_FORECAST_PATH = PROCESSED_DATA_DIR / "revenue_forecast.csv"
MODEL_COMPARISON_PATH = REPORTS_DIR / "model_comparison_results.csv"

CLASSIFIER_MODEL_PATH = MODELS_DIR / "churn_risk_classifier.pkl"
CLUSTERER_MODEL_PATH = MODELS_DIR / "customer_kmeans_clusterer.pkl"
FORECASTER_MODEL_PATH = MODELS_DIR / "revenue_forecaster.pkl"


# =====================================================================
# FILE VALIDATION
# =====================================================================

def _validate_file_exists(file_path: Path) -> None:
    """
    Verify that a required project file exists.

    Raises
    ------
    FileNotFoundError
        If the required file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required project file was not found:\n{file_path}"
        )


# =====================================================================
# MASTER DATA
# =====================================================================

@st.cache_data(show_spinner=False)
def load_master_data() -> pd.DataFrame:
    """
    Load the processed Olist master dataset.
    Prioritizes fast columnar Parquet if available, falling back to CSV.

    Returns
    -------
    pandas.DataFrame
        Cleaned master dataset at order-item grain.
    """
    df = None
    if MASTER_PARQUET_PATH.exists():
        try:
            df = pd.read_parquet(MASTER_PARQUET_PATH)
        except Exception:
            df = None

    if df is None:
        _validate_file_exists(MASTER_DATA_PATH)
        df = pd.read_csv(
            MASTER_DATA_PATH,
            low_memory=False,
        )

    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date",
    ]

    for column in datetime_columns:
        if column in df.columns and not pd.api.types.is_datetime64_any_dtype(df[column]):
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    return df


# =====================================================================
# CUSTOMER SEGMENTS
# =====================================================================

@st.cache_data(show_spinner=False)
def load_customer_segments() -> pd.DataFrame:
    """
    Load the customer RFM segmentation dataset.
    Prioritizes fast columnar Parquet if available, falling back to CSV.

    Returns
    -------
    pandas.DataFrame
        Customer-level RFM and clustering results.
    """
    if CUSTOMER_SEGMENTS_PARQUET_PATH.exists():
        try:
            return pd.read_parquet(CUSTOMER_SEGMENTS_PARQUET_PATH)
        except Exception:
            pass

    _validate_file_exists(CUSTOMER_SEGMENTS_PATH)

    df = pd.read_csv(
        CUSTOMER_SEGMENTS_PATH,
        low_memory=False,
    )

    return df


# =====================================================================
# MULTI-GRAIN REVENUE FORECAST
# =====================================================================

@st.cache_data(show_spinner=False)
def load_revenue_forecast(
    segment_type: Optional[str] = None,
    segment_value: Optional[str] = None,
) -> pd.DataFrame:
    """
    Load the multi-grain revenue forecasting results.

    Parameters
    ----------
    segment_type:
        Optional grain type filter: 'total', 'category', or 'region'.
    segment_value:
        Optional specific segment name (e.g., 'All', 'bed_bath_table', 'SP').

    Returns
    -------
    pandas.DataFrame
        Forecast dataframe with columns:
        [month, segment_type, segment_value, predicted_revenue,
         lower_bound, upper_bound, actual_revenue]
    """
    _validate_file_exists(REVENUE_FORECAST_PATH)

    df = pd.read_csv(
        REVENUE_FORECAST_PATH,
        low_memory=False,
    )

    if "month" in df.columns:
        df["month"] = pd.to_datetime(
            df["month"],
            errors="coerce",
        )

    # Apply optional filtering
    if segment_type:
        df = df[df["segment_type"] == segment_type]

    if segment_value:
        df = df[df["segment_value"] == segment_value]

    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def get_available_forecast_segments() -> Dict[str, List[str]]:
    """
    Extract all available forecast grain types and their corresponding segment values.

    Returns
    -------
    dict
        Mapping of grain_type -> list of available segment values.
    """
    df = load_revenue_forecast()

    if "segment_type" not in df.columns or "segment_value" not in df.columns:
        return {"total": ["All"]}

    segments_map = {}
    for stype in ["total", "category", "region"]:
        subset = df[df["segment_type"] == stype]
        if not subset.empty:
            segments_map[stype] = subset["segment_value"].dropna().unique().tolist()

    return segments_map


# =====================================================================
# MODEL COMPARISON
# =====================================================================

@st.cache_data(show_spinner=False)
def load_model_comparison() -> pd.DataFrame:
    """
    Load classification model comparison results (Logistic Regression,
    Random Forest, Gradient Boosting).

    Returns
    -------
    pandas.DataFrame
        Accuracy, precision, recall and F1-score for each model.
    """
    _validate_file_exists(MODEL_COMPARISON_PATH)

    df = pd.read_csv(
        MODEL_COMPARISON_PATH,
        low_memory=False,
    )

    return df


# =====================================================================
# PERSISTED ML MODEL ARTIFACTS
# =====================================================================

@st.cache_resource(show_spinner=False)
def load_classification_model() -> Dict[str, Any]:
    """
    Load the serialized champion dissatisfaction risk classifier artifact.

    Returns
    -------
    dict
        Contains:
        - 'model_name': str
        - 'model': trained scikit-learn classifier
        - 'feature_cols': list[str]
        - 'numeric_features': list[str]
        - 'top_categories': list[str]
        - 'feature_importances': list[dict]
        - 'metrics': dict
    """
    _validate_file_exists(CLASSIFIER_MODEL_PATH)
    return joblib.load(CLASSIFIER_MODEL_PATH)


@st.cache_resource(show_spinner=False)
def load_clustering_model() -> Dict[str, Any]:
    """
    Load the serialized KMeans RFM customer segmentation artifact.

    Returns
    -------
    dict
        Contains:
        - 'scaler': StandardScaler
        - 'kmeans': KMeans model
        - 'rfm_cols': list[str]
        - 'cluster_centers_raw': dict
        - 'segment_names': dict
    """
    _validate_file_exists(CLUSTERER_MODEL_PATH)
    return joblib.load(CLUSTERER_MODEL_PATH)


@st.cache_resource(show_spinner=False)
def load_forecasting_metadata() -> Dict[str, Any]:
    """
    Load forecasting metadata and model attributes.
    """
    _validate_file_exists(FORECASTER_MODEL_PATH)
    return joblib.load(FORECASTER_MODEL_PATH)


def predict_dissatisfaction_risk(
    delivery_delay_days: float,
    delivery_time_days: float,
    price: float,
    freight_value: float,
    payment_installments: float,
    product_category: str,
) -> Dict[str, Any]:
    """
    Predict customer low-review dissatisfaction risk for an order in real-time
    using the serialized champion classifier artifact.

    Returns
    -------
    dict
        - 'is_high_risk': bool
        - 'risk_probability': float (0.0 to 1.0)
        - 'risk_label': 'High Risk (Low Review Likely)' or 'Normal / Low Risk'
        - 'dominant_driver': str
    """
    model_artifact = load_classification_model()
    model = model_artifact["model"]
    feature_cols = model_artifact["feature_cols"]
    top_categories = model_artifact["top_categories"]

    # Construct feature row
    row = {
        "delivery_delay_days": float(delivery_delay_days),
        "delivery_time_days": float(delivery_time_days),
        "price": float(price),
        "freight_value": float(freight_value),
        "payment_installments": float(payment_installments),
    }

    # One-hot encoded categories
    category_grouped = product_category if product_category in top_categories else "other"
    for cat in top_categories:
        col_name = f"cat_{cat}"
        row[col_name] = (category_grouped == cat)
    row["cat_other"] = (category_grouped == "other")

    # Align with model columns
    feature_df = pd.DataFrame([row])
    for col in feature_cols:
        if col not in feature_df.columns:
            feature_df[col] = False
    feature_df = feature_df[feature_cols]

    # Predict
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(feature_df)[0][1])
    else:
        prob = float(model.predict(feature_df)[0])

    is_high_risk = prob >= 0.40  # Balanced operational threshold

    # Identify primary driver
    if delivery_delay_days > 0:
        driver = f"Late delivery by {delivery_delay_days:.0f} days vs SLA"
    elif delivery_time_days > 20:
        driver = f"Extended transit time ({delivery_time_days:.0f} days)"
    elif freight_value > 40:
        driver = f"High freight friction (R${freight_value:.2f})"
    else:
        driver = "Standard order parameters"

    return {
        "is_high_risk": is_high_risk,
        "risk_probability": prob,
        "risk_score_percent": prob * 100,
        "risk_label": "High Risk (Low Review Likely)" if is_high_risk else "Low Risk (Satisfied Review Likely)",
        "dominant_driver": driver,
    }


# =====================================================================
# DATASET SUMMARY
# =====================================================================

def get_dataset_summary() -> dict:
    """
    Return basic health metrics for the available datasets.
    """
    master_df = load_master_data()
    segments_df = load_customer_segments()
    forecast_df = load_revenue_forecast()

    return {
        "master_rows": len(master_df),
        "master_columns": len(master_df.columns),
        "orders": master_df["order_id"].nunique(),
        "customers": master_df["customer_unique_id"].nunique(),
        "segment_customers": len(segments_df),
        "forecast_periods": len(forecast_df),
    }