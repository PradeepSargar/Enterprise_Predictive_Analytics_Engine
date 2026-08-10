"""
Unit tests for Machine Learning model artifacts and inference
=============================================================
Tests classification and clustering models serialized in models/.
"""

import numpy as np
import pytest

from dashboards.data.loader import (
    load_classification_model,
    load_clustering_model,
    load_model_comparison,
    predict_dissatisfaction_risk,
)


class TestMachineLearningModels:

    def test_model_comparison_three_models_ranking(self):
        df = load_model_comparison()
        assert len(df) == 3

        # Confirm Random Forest has highest F1 Score (0.430)
        rf_row = df[df["Model"] == "Random Forest"].iloc[0]
        lr_row = df[df["Model"] == "Logistic Regression"].iloc[0]
        gb_row = df[df["Model"] == "Gradient Boosting"].iloc[0]

        assert rf_row["F1 Score"] >= lr_row["F1 Score"]
        assert rf_row["F1 Score"] >= gb_row["F1 Score"]
        assert gb_row["Accuracy"] > lr_row["Accuracy"]

    def test_classification_champion_pipeline(self):
        artifact = load_classification_model()
        model = artifact["model"]
        feature_cols = artifact["feature_cols"]

        assert hasattr(model, "predict")
        assert len(feature_cols) >= 15

        # Test dummy input vector
        dummy_X = np.zeros((1, len(feature_cols)))
        pred = model.predict(dummy_X)
        assert pred[0] in [0, 1]

    def test_clustering_kmeans_pipeline(self):
        artifact = load_clustering_model()
        kmeans = artifact["kmeans"]
        scaler = artifact["scaler"]

        assert kmeans.n_clusters == 4
        assert hasattr(scaler, "transform")

        # Test scaling and clustering on sample RFM
        sample_rfm = np.array([[180.0, 1.0, 200.0], [450.0, 1.0, 200.0]])
        scaled = scaler.transform(sample_rfm)
        clusters = kmeans.predict(scaled)
        assert len(clusters) == 2
        assert all(c in [0, 1, 2, 3] for c in clusters)

    def test_predict_dissatisfaction_risk_bounds_and_categories(self):
        categories = ["bed_bath_table", "health_beauty", "auto", "unknown_category_test"]
        for cat in categories:
            res = predict_dissatisfaction_risk(
                delivery_delay_days=2.0,
                delivery_time_days=10.0,
                price=150.0,
                freight_value=25.0,
                payment_installments=2,
                product_category=cat,
            )
            assert 0.0 <= res["risk_probability"] <= 1.0
            assert isinstance(res["is_high_risk"], bool)
            assert isinstance(res["dominant_driver"], str)
