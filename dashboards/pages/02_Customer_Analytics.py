"""
Customer Analytics Dashboard.
=============================
Enterprise Predictive Analytics Engine

This page provides an analytical view of customer behavior,
RFM dynamics, customer lifetime spend distributions, and retention opportunities.

Responsibilities:
- Customer KPI layer & scale scorecard
- Customer segment mix & distribution
- Customer value analysis & purchase frequency
- RFM behavioral distributions
- Frequency vs monetary value relationship
- Retention & churn-prevention opportunities
- Formatted segment performance data table with CSV/Excel export
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

from dashboards.components.alerts import insight_card
from dashboards.components.charts import (
    donut_chart,
    histogram,
    horizontal_bar_chart,
    scatter_chart,
)
from dashboards.components.containers import panel
from dashboards.components.exports import csv_download, excel_download
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import page_header, section_header
from dashboards.data.loader import load_customer_segments
from dashboards.utils.html import render_html

# ============================================================================
# CONSTANTS
# ============================================================================

CURRENCY_SYMBOL = "R$"

# ============================================================================
# LOAD CUSTOMER DATA
# ============================================================================

customer_df = load_customer_segments()

if customer_df is None or customer_df.empty:
    st.warning("Customer segmentation data is currently unavailable.")
    st.stop()

customer_df = customer_df.copy()

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Customer Analytics",
    description=(
        "Customer behavior, RFM segmentation, lifetime value distribution, "
        "and retention opportunity intelligence."
    ),
    status="CUSTOMER INTELLIGENCE",
)

render_html(
    """
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 40%, #8B5CF6 100%);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px -4px rgba(14, 165, 233, 0.25);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="position: relative; z-index: 2; max-width: 820px;">
            <div style="
                display: inline-block;
                padding: 0.25rem 0.6rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                font-size: 8.5px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            ">
                BEHAVIORAL RFM INTELLIGENCE
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Customer Lifetime Spend & Retention Dynamics
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F0F9FF;">
                Analyze Brazilian e-commerce customer concentration, repeat purchase frequency,
                and recency decay across verified customer cohorts.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# DATA PREPARATION
# ============================================================================

for column in ("recency", "frequency", "monetary"):
    if column in customer_df.columns:
        customer_df[column] = pd.to_numeric(customer_df[column], errors="coerce")

customer_df = customer_df.dropna(subset=["customer_unique_id", "segment"])

# ============================================================================
# SEGMENT FILTER TOOLBAR
# ============================================================================

section_header(
    title="Analysis Controls",
    description="Filter customer cohorts by specific RFM segment profiles.",
)

available_segments = sorted(
    customer_df["segment"].dropna().astype(str).unique().tolist()
)
segment_options = ["All Segments", *available_segments]

col_filter, col_metric = st.columns([1, 1], gap="medium")

with col_filter:
    selected_segment = st.selectbox(
        "Segment Focus",
        options=segment_options,
        index=0,
        help="Focus analytical distributions on a specific behavioral group.",
    )

if selected_segment == "All Segments":
    filtered_customers = customer_df.copy()
else:
    filtered_customers = customer_df[
        customer_df["segment"].astype(str) == selected_segment
    ].copy()

if filtered_customers.empty:
    st.warning("No customers are available for the selected segment.")
    st.stop()

with col_metric:
    st.info(
        f"**Active Cohort:** {selected_segment} — "
        f"**{len(filtered_customers):,}** active customer profiles analyzed."
    )

# ============================================================================
# KPI CALCULATIONS
# ============================================================================

total_customers = int(filtered_customers["customer_unique_id"].nunique())
repeat_customers = int((filtered_customers["frequency"] > 1).sum())
repeat_customer_rate = repeat_customers / total_customers if total_customers > 0 else 0
average_frequency = float(filtered_customers["frequency"].mean())
average_monetary = float(filtered_customers["monetary"].mean())
average_recency = float(filtered_customers["recency"].mean())
median_monetary = float(filtered_customers["monetary"].median())
total_cohort_gmv = float(filtered_customers["monetary"].sum())

# ============================================================================
# CUSTOMER KPI OVERVIEW
# ============================================================================

section_header(
    title="Customer KPI Overview",
    description="Core customer behavioral metrics calculated from the selected cohort.",
)

kpi_columns = st.columns(5, gap="small")

with kpi_columns[0]:
    kpi_card(
        label="Total Customers",
        value=f"{total_customers:,}",
        delta="Unique customer IDs",
        delta_type="neutral",
    )

with kpi_columns[1]:
    kpi_card(
        label="Repeat Purchase Rate",
        value=f"{repeat_customer_rate:.1%}",
        delta=f"{repeat_customers:,} repeat buyers",
        delta_type="positive" if repeat_customer_rate >= 0.05 else "warning",
    )

with kpi_columns[2]:
    kpi_card(
        label="Avg Order Frequency",
        value=f"{average_frequency:.2f}",
        delta="Orders per buyer",
        delta_type="neutral",
    )

with kpi_columns[3]:
    kpi_card(
        label="Avg Customer Spend",
        value=f"{CURRENCY_SYMBOL} {average_monetary:,.2f}",
        delta=f"Median: {CURRENCY_SYMBOL} {median_monetary:,.0f}",
        delta_type="positive",
    )

with kpi_columns[4]:
    kpi_card(
        label="Avg Inactivity Recency",
        value=f"{average_recency:.0f} days",
        delta="Days since last purchase",
        delta_type="positive" if average_recency <= 180 else "negative",
    )

# ============================================================================
# SEGMENT SUMMARY DATA & VISUALS
# ============================================================================

segment_summary = (
    customer_df.groupby("segment", as_index=False)
    .agg(
        customers=("customer_unique_id", "nunique"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_monetary=("monetary", "sum"),
    )
)

segment_summary["customer_share"] = (
    segment_summary["customers"] / segment_summary["customers"].sum()
)

section_header(
    title="Customer Segmentation & Behavioral Mix",
    description="Understand customer concentration, relative scale, and average spend by group.",
)

seg_col1, seg_col2 = st.columns([1.0, 1.15], gap="large")

with seg_col1:
    with panel(
        title="Customer Segment Mix",
        description="Share of total customer base by RFM cluster.",
    ):
        donut_chart(
            dataframe=segment_summary,
            names="segment",
            values="customers",
            title="Customer Segment Distribution",
            height=370,
        )

with seg_col2:
    with panel(
        title="Segment Population Scale",
        description="Total unique buyers categorized in each segment.",
    ):
        segment_scale = segment_summary[["segment", "customers"]].sort_values(
            "customers", ascending=True
        )
        horizontal_bar_chart(
            dataframe=segment_scale,
            category="segment",
            value="customers",
            title="Customer Count by Segment",
            category_title="Segment",
            value_title="Customers",
            height=370,
            text=True,
        )

# ============================================================================
# CUSTOMER VALUE & RFM DEEP DIVE
# ============================================================================

section_header(
    title="Customer Value & RFM Behavioral Distribution",
    description="Examine recency, frequency, and monetary distributions at the individual buyer level.",
)

rfm_col1, rfm_col2, rfm_col3 = st.columns(3, gap="medium")

with rfm_col1:
    with panel(
        title="Recency Distribution",
        description="Days elapsed since the customer's last order.",
    ):
        histogram(
            dataframe=filtered_customers,
            column="recency",
            title="Recency Distribution",
            x_title="Days Inactive",
            y_title="Customers",
            bins=30,
            height=320,
        )

with rfm_col2:
    with panel(
        title="Frequency Distribution",
        description="Number of lifetime completed orders per customer.",
    ):
        histogram(
            dataframe=filtered_customers,
            column="frequency",
            title="Order Frequency",
            x_title="Lifetime Orders",
            y_title="Customers",
            bins=20,
            height=320,
        )

with rfm_col3:
    with panel(
        title="Monetary Value Distribution",
        description="Total gross spend across all orders (BRL).",
    ):
        histogram(
            dataframe=filtered_customers,
            column="monetary",
            title="Monetary Spend",
            x_title="Total Spend (R$)",
            y_title="Customers",
            bins=30,
            height=320,
        )

# ============================================================================
# VALUE RELATIONSHIPS & SCATTER
# ============================================================================

section_header(
    title="Customer Spend vs Frequency Relationships",
    description="Evaluate high-value customer clusters and frequency correlations.",
)

rel_col1, rel_col2 = st.columns([1.7, 1.0], gap="large")

with rel_col1:
    with panel(
        title="Purchase Frequency vs Lifetime Value",
        description="Scatter relationship highlighting high-monetary clusters.",
    ):
        scatter_chart(
            dataframe=filtered_customers,
            x="frequency",
            y="monetary",
            color="segment",
            title="Order Frequency vs Customer Spend (R$)",
            x_title="Lifetime Frequency",
            y_title="Monetary Value (R$)",
            height=400,
            opacity=0.7,
        )

with rel_col2:
    with panel(
        title="Average Segment Value",
        description="Mean lifetime gross expenditure per segment.",
    ):
        val_by_seg = segment_summary[["segment", "avg_monetary"]].sort_values(
            "avg_monetary", ascending=True
        )
        horizontal_bar_chart(
            dataframe=val_by_seg,
            category="segment",
            value="avg_monetary",
            title="Avg Spend by Segment (R$)",
            category_title="Segment",
            value_title="Avg Value (R$)",
            height=400,
            text=True,
        )

# ============================================================================
# RETENTION OPPORTUNITIES & STRATEGIC PLAYBOOK
# ============================================================================

section_header(
    title="Retention Opportunities & Actionable Insights",
    description="Prioritize conversion workflows based on customer lifetime value and lapse risk.",
)

one_time_count = int(
    customer_df[customer_df["segment"].isin({"Recent One-Time Buyers"})].shape[0]
)
risk_count = int(
    customer_df[
        customer_df["segment"].isin({"Lapsed / At Risk", "At Risk", "Lapsed"})
    ].shape[0]
)
high_value_count = int(
    customer_df[
        customer_df["segment"].astype(str).str.contains("High-Value", case=False, na=False)
    ].shape[0]
)
total_base = int(customer_df["customer_unique_id"].nunique())

one_time_share = one_time_count / total_base if total_base > 0 else 0
risk_share = risk_count / total_base if total_base > 0 else 0
high_value_share = high_value_count / total_base if total_base > 0 else 0

ret_col1, ret_col2, ret_col3 = st.columns(3, gap="medium")

with ret_col1:
    insight_card(
        label="SECOND-ORDER CONVERSION",
        title="One-Time Buyer Nurturing",
        description=(
            f"{one_time_count:,} buyers ({one_time_share:.1%} of marketplace) "
            "are recent one-time purchasers. Automated post-delivery re-engagement "
            "campaigns represent the highest ROI opportunity."
        ),
        insight_type="warning",
    )

with ret_col2:
    insight_card(
        label="CHURN MITIGATION",
        title="Lapsed Customer Win-Back",
        description=(
            f"{risk_count:,} customers ({risk_share:.1%} of marketplace) "
            "fall into dormant cohorts with >200 days of inactivity. "
            "Targeted discount incentives can reactivate high-intent buyers."
        ),
        insight_type="danger" if risk_share >= 0.10 else "warning",
    )

with ret_col3:
    insight_card(
        label="VIP ADVOCACY",
        title="Protect High-Value Customers",
        description=(
            f"{high_value_count:,} customers ({high_value_share:.1%} of marketplace) "
            "generate a disproportionate share of cumulative GMV. "
            "Assign priority logistics SLAs and premium customer support."
        ),
        insight_type="success",
    )

# ============================================================================
# SEGMENT PERFORMANCE DATA TABLE & EXPORTS
# ============================================================================

section_header(
    title="Segment Performance Master Table",
    description="Comprehensive summary metrics across all customer segmentation groups.",
)

with panel(
    title="Segment Performance Table",
    description="Granular performance table formatted with Brazilian Real (R$) currency and customer counts.",
):
    table_df = segment_summary.copy()
    table_df = table_df.rename(
        columns={
            "segment": "Segment",
            "customers": "Total Customers",
            "customer_share": "Marketplace Share",
            "avg_recency": "Avg Recency (Days)",
            "avg_frequency": "Avg Orders",
            "avg_monetary": "Avg Spend (R$)",
            "total_monetary": "Total GMV (R$)",
        }
    )

    st.dataframe(
        table_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Marketplace Share": st.column_config.ProgressColumn(
                "Marketplace Share",
                format="%.1f%%",
                min_value=0.0,
                max_value=1.0,
            ),
            "Avg Spend (R$)": st.column_config.NumberColumn(
                "Avg Spend",
                format="R$ %.2f",
            ),
            "Total GMV (R$)": st.column_config.NumberColumn(
                "Total GMV",
                format="R$ %.2f",
            ),
            "Avg Orders": st.column_config.NumberColumn(
                "Avg Orders",
                format="%.2f",
            ),
            "Avg Recency (Days)": st.column_config.NumberColumn(
                "Avg Recency",
                format="%.0f days",
            ),
            "Total Customers": st.column_config.NumberColumn(
                "Customers",
                format="%d",
            ),
        },
    )

    col_exp1, col_exp2, col_spacer = st.columns([1, 1, 2], gap="small")
    with col_exp1:
        csv_download(table_df, filename="customer_segments_summary.csv", key="csv_cust_seg")
    with col_exp2:
        excel_download(table_df, filename="customer_segments_summary.xlsx", key="excel_cust_seg")