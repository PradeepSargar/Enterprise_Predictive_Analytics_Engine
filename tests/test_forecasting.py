"""
Unit tests for multi-grain time-series forecasting integrity
============================================================
Validates multi-grain cuts, forecast horizons, confidence bounds, and consistency.
"""

import pandas as pd
import pytest

from dashboards.data.loader import get_available_forecast_segments, load_revenue_forecast
from dashboards.data.transformations import prepare_revenue_forecast


class TestForecasting:

    def test_multi_grain_segments_completeness(self):
        segments_map = get_available_forecast_segments()
        assert "total" in segments_map
        assert "category" in segments_map
        assert "region" in segments_map

        # Verify each segment cut has 26 rows (20 history + 6 future)
        for stype, values in segments_map.items():
            for val in values:
                df = load_revenue_forecast(segment_type=stype, segment_value=val)
                assert len(df) == 26, f"Segment {stype}:{val} does not have 26 monthly periods"
                assert df["predicted_revenue"].notna().all()
                assert df["lower_bound"].notna().all()
                assert df["upper_bound"].notna().all()

                # Exactly 6 future forecast periods
                future_rows = df[df["actual_revenue"].isna()]
                assert len(future_rows) == 6

                # Exactly 20 historical periods
                hist_rows = df[df["actual_revenue"].notna()]
                assert len(hist_rows) == 20

    def test_total_forecast_regression_check(self):
        """
        Verify that total forecast numbers match the expected baseline point estimates.
        """
        df_total = load_revenue_forecast(segment_type="total", segment_value="All")
        future_total = df_total[df_total["actual_revenue"].isna()].sort_values("month")

        # Sept 2018 - Feb 2019 point estimate checks (approximate within 1% due to sampling variations)
        expected_sept = 1655885
        actual_sept = future_total.iloc[0]["predicted_revenue"]
        assert actual_sept == pytest.approx(expected_sept, rel=0.01)

        expected_feb = 1976475
        actual_feb = future_total.iloc[-1]["predicted_revenue"]
        assert actual_feb == pytest.approx(expected_feb, rel=0.01)

    def test_confidence_bounds_logic(self):
        df = load_revenue_forecast()
        # Lower bound should always be <= Upper bound
        assert (df["lower_bound"] <= df["upper_bound"] + 1e-3).all()
        # All lower bounds should be non-negative
        assert (df["lower_bound"] >= 0.0).all()
