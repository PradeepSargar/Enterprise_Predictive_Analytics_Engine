"""
Unit tests for executive KPI calculations & order deduplication
==============================================================
Tests dashboards/data/transformations.py (KPI & order-level logic).
"""

import pandas as pd
import pytest

from dashboards.data.loader import load_master_data
from dashboards.data.transformations import (
    build_order_level_data,
    calculate_executive_kpis,
)


class TestExecutiveKPIs:

    def test_build_order_level_data_deduplication(self):
        # Create synthetic multi-item orders
        data = {
            "order_id": ["O1", "O1", "O2", "O3", "O3", "O3"],
            "customer_unique_id": ["C1", "C1", "C2", "C3", "C3", "C3"],
            "payment_value": [50.0, 50.0, 120.0, 30.0, 30.0, 30.0],
            "review_score": [5.0, 5.0, 1.0, 4.0, 4.0, 4.0],
        }
        df = pd.DataFrame(data)

        order_df = build_order_level_data(df)
        assert len(order_df) == 3
        assert list(order_df["order_id"]) == ["O1", "O2", "O3"]

    def test_build_order_level_data_validation(self):
        with pytest.raises(ValueError):
            build_order_level_data(None)

        with pytest.raises(ValueError):
            build_order_level_data(pd.DataFrame({"invalid_col": [1, 2]}))

        empty_df = pd.DataFrame(columns=["order_id", "customer_unique_id"])
        res_empty = build_order_level_data(empty_df)
        assert res_empty.empty

    def test_calculate_executive_kpis_real_data(self):
        master_df = load_master_data()
        kpis = calculate_executive_kpis(master_df)

        assert isinstance(kpis, dict)
        assert kpis["total_orders"] > 90000
        assert kpis["total_customers"] > 90000
        assert kpis["total_revenue"] > 10000000
        assert kpis["average_order_value"] > 50
        assert 0.0 <= kpis["repeat_customer_rate"] <= 1.0
        assert 1.0 <= kpis["average_review_score"] <= 5.0
        assert 0.0 <= kpis["low_review_rate"] <= 1.0

    def test_calculate_executive_kpis_empty_and_synthetic(self):
        empty_df = pd.DataFrame(columns=["order_id", "customer_unique_id", "payment_value", "review_score"])
        empty_kpis = calculate_executive_kpis(empty_df)
        assert empty_kpis["total_orders"] == 0
        assert empty_kpis["total_revenue"] == 0.0

        # Synthetic test with 1 repeat customer out of 2
        df_syn = pd.DataFrame({
            "order_id": ["O1", "O2", "O3"],
            "customer_unique_id": ["C1", "C1", "C2"],
            "payment_value": [100.0, 200.0, 300.0],
            "review_score": [5.0, 1.0, 2.0],
        })
        kpis_syn = calculate_executive_kpis(df_syn)
        assert kpis_syn["total_orders"] == 3
        assert kpis_syn["total_customers"] == 2
        assert kpis_syn["total_revenue"] == 600.0
        assert kpis_syn["average_order_value"] == 200.0
        assert kpis_syn["repeat_customer_rate"] == 0.5
        assert kpis_syn["low_review_rate"] == pytest.approx(2 / 3)
