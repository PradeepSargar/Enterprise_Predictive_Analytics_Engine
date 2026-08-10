"""
Unit tests for business transformations
=======================================
Tests dashboards/data/transformations.py (monthly aggregation, forecast prep).
"""

import pandas as pd
import pytest

from dashboards.data.loader import load_master_data, load_revenue_forecast
from dashboards.data.transformations import (
    calculate_monthly_business_performance,
    prepare_revenue_forecast,
)


class TestTransformations:

    def test_calculate_monthly_business_performance(self):
        master_df = load_master_data()
        monthly = calculate_monthly_business_performance(master_df)

        assert isinstance(monthly, pd.DataFrame)
        assert len(monthly) >= 20

        cols = ["month", "revenue", "orders", "average_order_value"]
        for col in cols:
            assert col in monthly.columns

        assert (monthly["revenue"] >= 0).all()
        assert (monthly["orders"] >= 0).all()
        assert (monthly["average_order_value"] >= 0).all()

        # Check chronological order
        assert monthly["month"].is_monotonic_increasing

    def test_prepare_revenue_forecast(self):
        raw_fc = load_revenue_forecast(segment_type="total", segment_value="All")
        prepared = prepare_revenue_forecast(raw_fc)

        assert isinstance(prepared, pd.DataFrame)
        assert len(prepared) == 26

        # Check column types
        assert pd.api.types.is_datetime64_any_dtype(prepared["month"])
        assert pd.api.types.is_numeric_dtype(prepared["predicted_revenue"])
        assert pd.api.types.is_numeric_dtype(prepared["lower_bound"])
        assert pd.api.types.is_numeric_dtype(prepared["upper_bound"])

        # Check sorting
        assert prepared["month"].is_monotonic_increasing

    def test_transformation_exceptions_and_empty(self):
        with pytest.raises(ValueError):
            calculate_monthly_business_performance(pd.DataFrame({"invalid": [1]}))

        with pytest.raises(ValueError):
            prepare_revenue_forecast(None)

        with pytest.raises(ValueError):
            prepare_revenue_forecast(pd.DataFrame({"invalid": [1]}))

        empty_master = pd.DataFrame(columns=["order_id", "customer_unique_id", "order_purchase_timestamp", "payment_value"])
        assert calculate_monthly_business_performance(empty_master).empty
