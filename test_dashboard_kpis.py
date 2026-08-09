"""
Validation script for executive KPI calculations.

This test verifies that order-level deduplication and business
KPI calculations are working as expected.
"""

from dashboards.data.loader import load_master_data

from dashboards.data.transformations import (
    build_order_level_data,
    calculate_executive_kpis,
)


# ---------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------

master_df = load_master_data()


# ---------------------------------------------------------------------
# BUILD ORDER-LEVEL DATA
# ---------------------------------------------------------------------

order_df = build_order_level_data(master_df)


# ---------------------------------------------------------------------
# CALCULATE KPIs
# ---------------------------------------------------------------------

kpis = calculate_executive_kpis(master_df)


# ---------------------------------------------------------------------
# VALIDATION OUTPUT
# ---------------------------------------------------------------------

print("\n========== KPI VALIDATION ==========")

print(
    f"Master rows: "
    f"{len(master_df):,}"
)

print(
    f"Order-level rows: "
    f"{len(order_df):,}"
)

print(
    f"Unique orders: "
    f"{kpis['total_orders']:,}"
)

print(
    f"Unique customers: "
    f"{kpis['total_customers']:,}"
)

print(
    f"Total revenue: "
    f"₹{kpis['total_revenue']:,.2f}"
)

print(
    f"Average order value: "
    f"₹{kpis['average_order_value']:,.2f}"
)

print(
    f"Repeat customer rate: "
    f"{kpis['repeat_customer_rate']:.2%}"
)

print(
    f"Average review score: "
    f"{kpis['average_review_score']:.2f}"
)

print(
    f"Low review rate: "
    f"{kpis['low_review_rate']:.2%}"
)


# ---------------------------------------------------------------------
# BASIC SANITY CHECKS
# ---------------------------------------------------------------------

assert len(order_df) == kpis["total_orders"]

assert kpis["total_revenue"] > 0

assert kpis["total_customers"] > 0

assert 0 <= kpis["repeat_customer_rate"] <= 1

assert 0 <= kpis["low_review_rate"] <= 1


print("\n========== KPI VALIDATION PASSED ==========")
