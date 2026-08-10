"""
Unit tests for dashboards/data/loader.py
=======================================
Validates dataset loading, date parsing, model deserialization,
multi-grain forecast filtering, and error handling.
"""

from pathlib import Path
import pandas as pd
import pytest

from dashboards.data.loader import (
    get_available_forecast_segments,
    get_dataset_summary,
    load_classification_model,
    load_clustering_model,
    load_customer_segments,
    load_forecasting_metadata,
    load_master_data,
    load_model_comparison,
    load_revenue_forecast,
    predict_dissatisfaction_risk,
    _validate_file_exists,
)


class TestDataLoader:

    def test_load_master_data_schema_and_types(self):
        df = load_master_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 100000

        # Check required columns
        expected_cols = [
            "order_id",
            "customer_unique_id",
            "order_purchase_timestamp",
            "payment_value",
            "review_score",
            "delivery_delay_days",
            "delivery_time_days",
        ]
        for col in expected_cols:
            assert col in df.columns, f"Missing expected column: {col}"

        # Check datetime conversion
        assert pd.api.types.is_datetime64_any_dtype(df["order_purchase_timestamp"])

    def test_load_customer_segments_schema(self):
        df = load_customer_segments()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 90000

        required_cols = ["customer_unique_id", "recency", "frequency", "monetary", "segment"]
        for col in required_cols:
            assert col in df.columns, f"Missing RFM segment column: {col}"

        # Validate segments present
        unique_segments = set(df["segment"].dropna().unique())
        assert len(unique_segments) >= 4

    def test_load_revenue_forecast_all_and_filtered(self):
        # Full multi-grain forecast
        df_all = load_revenue_forecast()
        assert isinstance(df_all, pd.DataFrame)
        assert len(df_all) > 200

        cols = [
            "month",
            "segment_type",
            "segment_value",
            "predicted_revenue",
            "lower_bound",
            "upper_bound",
            "actual_revenue",
        ]
        for col in cols:
            assert col in df_all.columns

        # Filter by total
        df_total = load_revenue_forecast(segment_type="total", segment_value="All")
        assert len(df_total) == 26
        assert (df_total["segment_type"] == "total").all()
        assert (df_total["segment_value"] == "All").all()

        # Filter by category
        df_cat = load_revenue_forecast(segment_type="category", segment_value="bed_bath_table")
        assert len(df_cat) == 26
        assert (df_cat["segment_value"] == "bed_bath_table").all()

        # Filter by region
        df_region = load_revenue_forecast(segment_type="region", segment_value="SP")
        assert len(df_region) == 26
        assert (df_region["segment_value"] == "SP").all()

    def test_get_available_forecast_segments(self):
        segments_map = get_available_forecast_segments()
        assert "total" in segments_map
        assert "category" in segments_map
        assert "region" in segments_map
        assert "All" in segments_map["total"]
        assert len(segments_map["category"]) == 5
        assert len(segments_map["region"]) == 5

    def test_load_model_comparison(self):
        df = load_model_comparison()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3  # Logistic Regression, Random Forest, Gradient Boosting

        expected_models = {"Logistic Regression", "Random Forest", "Gradient Boosting"}
        assert set(df["Model"].unique()) == expected_models

        for metric in ["Accuracy", "Precision", "Recall", "F1 Score"]:
            assert metric in df.columns
            assert ((df[metric] >= 0.0) & (df[metric] <= 1.0)).all()

    def test_load_serialized_models(self):
        clf_artifact = load_classification_model()
        assert "model" in clf_artifact
        assert "feature_cols" in clf_artifact
        assert clf_artifact["model_name"] == "Random Forest"

        cluster_artifact = load_clustering_model()
        assert "kmeans" in cluster_artifact
        assert "scaler" in cluster_artifact
        assert len(cluster_artifact["rfm_cols"]) == 3

        fc_meta = load_forecasting_metadata()
        assert "grain_types" in fc_meta
        assert fc_meta["forecast_periods"] == 6

    def test_predict_dissatisfaction_risk_utility(self):
        # Scenario 1: On-time delivery, standard order
        res_normal = predict_dissatisfaction_risk(
            delivery_delay_days=-5.0,
            delivery_time_days=7.0,
            price=80.0,
            freight_value=15.0,
            payment_installments=1,
            product_category="health_beauty",
        )
        assert "risk_probability" in res_normal
        assert 0.0 <= res_normal["risk_probability"] <= 1.0
        assert not res_normal["is_high_risk"]

        # Scenario 2: Severe delivery delay
        res_delayed = predict_dissatisfaction_risk(
            delivery_delay_days=15.0,
            delivery_time_days=30.0,
            price=200.0,
            freight_value=45.0,
            payment_installments=3,
            product_category="bed_bath_table",
        )
        assert res_delayed["risk_probability"] > res_normal["risk_probability"]
        assert res_delayed["is_high_risk"]
        assert "Late delivery" in res_delayed["dominant_driver"]

    def test_dataset_summary(self):
        summary = get_dataset_summary()
        assert summary["master_rows"] > 0
        assert summary["orders"] > 90000
        assert summary["customers"] > 90000

    def test_validate_file_exists_raises_on_missing(self):
        with pytest.raises(FileNotFoundError):
            _validate_file_exists(Path("non_existent_directory/non_existent_file.csv"))
