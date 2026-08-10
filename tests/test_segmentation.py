"""
Unit tests for customer RFM segmentation logic
==============================================
Tests dashboards/data/transformations.py (RFM & clustering aggregation).
"""

import pandas as pd
import pytest

from dashboards.data.loader import load_customer_segments
from dashboards.data.transformations import (
    calculate_customer_segment_summary,
    calculate_rfm_summary,
    calculate_segment_performance,
)


class TestSegmentation:

    def test_calculate_customer_segment_summary(self):
        segments_df = load_customer_segments()
        summary = calculate_customer_segment_summary(segments_df)

        assert isinstance(summary, pd.DataFrame)
        assert len(summary) >= 4
        assert "segment" in summary.columns
        assert "customers" in summary.columns
        assert "percentage" in summary.columns
        assert summary["percentage"].sum() == pytest.approx(1.0, rel=1e-3)

    def test_calculate_segment_performance(self):
        segments_df = load_customer_segments()
        perf = calculate_segment_performance(segments_df)

        expected_cols = [
            "segment",
            "customers",
            "customer_share",
            "avg_recency",
            "avg_frequency",
            "avg_monetary",
            "total_monetary",
        ]
        for col in expected_cols:
            assert col in perf.columns

        assert (perf["avg_recency"] >= 0).all()
        assert (perf["avg_frequency"] >= 1.0).all()
        assert (perf["avg_monetary"] > 0).all()
        assert perf["customer_share"].sum() == pytest.approx(1.0, rel=1e-3)

    def test_calculate_rfm_summary(self):
        segments_df = load_customer_segments()
        rfm_sum = calculate_rfm_summary(segments_df)

        assert isinstance(rfm_sum, dict)
        assert "recency_median" in rfm_sum
        assert "frequency_median" in rfm_sum
        assert "monetary_median" in rfm_sum
        assert rfm_sum["recency_median"] > 0
        assert rfm_sum["frequency_median"] >= 1.0
        assert rfm_sum["monetary_median"] > 0

    def test_segmentation_edge_cases(self):
        with pytest.raises(ValueError):
            calculate_customer_segment_summary(None)

        with pytest.raises(ValueError):
            calculate_segment_performance(None)

        with pytest.raises(ValueError):
            calculate_rfm_summary(None)

        empty_df = pd.DataFrame(columns=["segment", "recency", "frequency", "monetary"])
        assert calculate_customer_segment_summary(empty_df).empty
        assert calculate_segment_performance(empty_df).empty
        empty_rfm = calculate_rfm_summary(empty_df)
        assert empty_rfm["recency_median"] == 0.0
