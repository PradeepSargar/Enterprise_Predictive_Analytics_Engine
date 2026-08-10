"""
Customer Analytics Dashboard.

This page provides a portfolio-quality analytical view of customer
behavior using the prepared RFM customer segmentation dataset.

Responsibilities
----------------
- Customer KPI analysis
- Customer segment distribution
- Customer value analysis
- RFM behavioral analysis
- Customer value relationships
- Retention opportunity analysis
- Segment-level business insights

Architecture
------------
Data loading:
    dashboards.data.loader

Visualization:
    dashboards.components.charts

UI:
    dashboards.components.kpi_cards
    dashboards.components.section_headers
    dashboards.components.alerts

No CSV files are loaded directly by this page.
No business metrics are hardcoded.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

from dashboards.components.alerts import (
    insight_card,
)

from dashboards.components.charts import (
    donut_chart,
    histogram,
    horizontal_bar_chart,
    scatter_chart,
)

from dashboards.components.kpi_cards import (
    kpi_card,
)

from dashboards.components.section_headers import (
    page_header,
    section_header,
)


# ============================================================================
# DATA LAYER
# ============================================================================

from dashboards.data.loader import (
    load_customer_segments,
)


# ============================================================================
# CONSTANTS
# ============================================================================

CURRENCY_SYMBOL = "R$"


# ============================================================================
# LOAD CUSTOMER DATA
# ============================================================================

customer_df = load_customer_segments()


# ============================================================================
# VALIDATE DATASET
# ============================================================================

if customer_df is None or customer_df.empty:

    st.warning(
        "Customer segmentation data is currently unavailable."
    )

    st.stop()


# Work on a copy so Streamlit's cached dataframe is never modified.

customer_df = customer_df.copy()


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="Customer Analytics",
    description=(
        "Customer behavior, RFM segmentation, customer value, "
        "and retention opportunities."
    ),
)


# ============================================================================
# DATA VALIDATION
# ============================================================================

required_columns = {
    "customer_unique_id",
    "segment",
    "recency",
    "frequency",
    "monetary",
}


missing_columns = (
    required_columns
    - set(customer_df.columns)
)


if missing_columns:

    st.error(
        "Customer segmentation data is missing required fields: "
        + ", ".join(sorted(missing_columns))
    )

    st.stop()


# ============================================================================
# DATA PREPARATION
# ============================================================================

for column in (
    "recency",
    "frequency",
    "monetary",
):

    customer_df[column] = pd.to_numeric(
        customer_df[column],
        errors="coerce",
    )


customer_df = customer_df.dropna(
    subset=[
        "customer_unique_id",
        "segment",
    ]
)


# ============================================================================
# SEGMENT FILTER
# ============================================================================

section_header(
    title="Analysis Controls",
    description=(
        "Focus the customer analysis on a specific RFM segment."
    ),
)


available_segments = sorted(
    customer_df["segment"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


segment_options = [
    "All Segments",
    *available_segments,
]


selected_segment = st.selectbox(
    "Segment Focus",
    options=segment_options,
    index=0,
)


# ============================================================================
# APPLY SEGMENT FILTER
# ============================================================================

if selected_segment == "All Segments":

    filtered_customers = customer_df.copy()

else:

    filtered_customers = customer_df[
        customer_df["segment"].astype(str)
        == selected_segment
    ].copy()


if filtered_customers.empty:

    st.warning(
        "No customers are available for the selected segment."
    )

    st.stop()


# ============================================================================
# KPI CALCULATIONS
# ============================================================================

total_customers = int(
    filtered_customers[
        "customer_unique_id"
    ].nunique()
)


repeat_customers = int(
    (
        filtered_customers["frequency"] > 1
    ).sum()
)


repeat_customer_rate = (
    repeat_customers / total_customers
    if total_customers > 0
    else 0
)


average_frequency = (
    filtered_customers["frequency"]
    .mean()
)


average_monetary = (
    filtered_customers["monetary"]
    .mean()
)


average_recency = (
    filtered_customers["recency"]
    .mean()
)


median_monetary = (
    filtered_customers["monetary"]
    .median()
)


# ============================================================================
# CUSTOMER KPI OVERVIEW
# ============================================================================

section_header(
    title="Customer KPI Overview",
    description=(
        "Core customer metrics calculated from the selected RFM population."
    ),
)


kpi_columns = st.columns(
    5,
    gap="small",
)


# ----------------------------------------------------------------------------
# Total Customers
# ----------------------------------------------------------------------------

with kpi_columns[0]:

    kpi_card(
        label="Total Customers",
        value=f"{total_customers:,}",
        delta=(
            "Entire customer base"
            if selected_segment == "All Segments"
            else selected_segment
        ),
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Repeat Customer Rate
# ----------------------------------------------------------------------------

with kpi_columns[1]:

    kpi_card(
        label="Repeat Customer Rate",
        value=f"{repeat_customer_rate:.1%}",
        delta="Customers with more than one order",
        delta_type=(
            "positive"
            if repeat_customer_rate >= 0.10
            else "negative"
        ),
    )


# ----------------------------------------------------------------------------
# Average Frequency
# ----------------------------------------------------------------------------

with kpi_columns[2]:

    kpi_card(
        label="Avg Purchase Frequency",
        value=f"{average_frequency:.2f}",
        delta="Orders per customer",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Average Customer Value
# ----------------------------------------------------------------------------

with kpi_columns[3]:

    kpi_card(
        label="Avg Customer Value",
        value=(
            f"{CURRENCY_SYMBOL}"
            f"{average_monetary:,.0f}"
        ),
        delta="Average monetary value",
        delta_type="positive",
    )


# ----------------------------------------------------------------------------
# Average Recency
# ----------------------------------------------------------------------------

with kpi_columns[4]:

    kpi_card(
        label="Avg Recency",
        value=f"{average_recency:.0f} days",
        delta="Days since purchase",
        delta_type=(
            "positive"
            if average_recency <= 180
            else "negative"
        ),
    )


# ============================================================================
# CUSTOMER SEGMENTATION
# ============================================================================

section_header(
    title="Customer Segmentation",
    description=(
        "Understand customer concentration and the relative scale "
        "of each RFM segment."
    ),
)


# ============================================================================
# SEGMENT SUMMARY DATA
# ============================================================================

segment_summary = (
    customer_df
    .groupby(
        "segment",
        as_index=False,
    )
    .agg(
        customers=(
            "customer_unique_id",
            "nunique",
        ),
        avg_recency=(
            "recency",
            "mean",
        ),
        avg_frequency=(
            "frequency",
            "mean",
        ),
        avg_monetary=(
            "monetary",
            "mean",
        ),
        total_monetary=(
            "monetary",
            "sum",
        ),
    )
)


segment_summary["customer_share"] = (
    segment_summary["customers"]
    / segment_summary["customers"].sum()
)


# ============================================================================
# SEGMENT VISUALS
# ============================================================================

segment_mix_col, segment_scale_col = st.columns(
    [1.0, 1.15],
    gap="large",
)


# ----------------------------------------------------------------------------
# Segment Mix
# ----------------------------------------------------------------------------

with segment_mix_col:

    donut_chart(
        dataframe=segment_summary,
        names="segment",
        values="customers",
        title="Customer Segment Mix",
        height=390,
    )


# ----------------------------------------------------------------------------
# Segment Scale
# ----------------------------------------------------------------------------

with segment_scale_col:

    segment_scale = (
        segment_summary[
            [
                "segment",
                "customers",
            ]
        ]
        .sort_values(
            "customers",
            ascending=True,
        )
    )


    horizontal_bar_chart(
        dataframe=segment_scale,
        category="segment",
        value="customers",
        title="Customer Count by Segment",
        category_title="Segment",
        value_title="Customers",
        height=390,
        text=True,
    )


# ============================================================================
# CUSTOMER VALUE ANALYSIS
# ============================================================================

section_header(
    title="Customer Value Analysis",
    description=(
        "Compare monetary value and purchase engagement across customer segments."
    ),
)


value_col, frequency_col = st.columns(
    2,
    gap="large",
)


# ----------------------------------------------------------------------------
# Average Monetary Value
# ----------------------------------------------------------------------------

with value_col:

    value_by_segment = (
        segment_summary[
            [
                "segment",
                "avg_monetary",
            ]
        ]
        .sort_values(
            "avg_monetary",
            ascending=True,
        )
    )


    horizontal_bar_chart(
        dataframe=value_by_segment,
        category="segment",
        value="avg_monetary",
        title="Average Customer Value by Segment",
        category_title="Segment",
        value_title="Average Value",
        height=380,
        text=True,
    )


# ----------------------------------------------------------------------------
# Average Purchase Frequency
# ----------------------------------------------------------------------------

with frequency_col:

    frequency_by_segment = (
        segment_summary[
            [
                "segment",
                "avg_frequency",
            ]
        ]
        .sort_values(
            "avg_frequency",
            ascending=True,
        )
    )


    horizontal_bar_chart(
        dataframe=frequency_by_segment,
        category="segment",
        value="avg_frequency",
        title="Average Purchase Frequency by Segment",
        category_title="Segment",
        value_title="Orders per Customer",
        height=380,
        text=True,
    )


# ============================================================================
# RFM BEHAVIOR
# ============================================================================

section_header(
    title="RFM Behavioral Analysis",
    description=(
        "Examine recency, purchase frequency, and monetary value "
        "at the customer level."
    ),
)


rfm_col1, rfm_col2, rfm_col3 = st.columns(
    3,
    gap="medium",
)


# ----------------------------------------------------------------------------
# Recency
# ----------------------------------------------------------------------------

with rfm_col1:

    histogram(
        dataframe=filtered_customers,
        column="recency",
        title="Recency Distribution",
        x_title="Days Since Last Purchase",
        y_title="Customers",
        bins=30,
        height=330,
    )


# ----------------------------------------------------------------------------
# Frequency
# ----------------------------------------------------------------------------

with rfm_col2:

    histogram(
        dataframe=filtered_customers,
        column="frequency",
        title="Purchase Frequency Distribution",
        x_title="Orders per Customer",
        y_title="Customers",
        bins=20,
        height=330,
    )


# ----------------------------------------------------------------------------
# Monetary
# ----------------------------------------------------------------------------

with rfm_col3:

    histogram(
        dataframe=filtered_customers,
        column="monetary",
        title="Monetary Value Distribution",
        x_title="Customer Value",
        y_title="Customers",
        bins=30,
        height=330,
    )


# ============================================================================
# RFM SUMMARY KPIs
# ============================================================================

rfm_summary_col1, rfm_summary_col2, rfm_summary_col3 = st.columns(
    3,
    gap="medium",
)


with rfm_summary_col1:

    kpi_card(
        label="Median Recency",
        value=(
            f"{filtered_customers['recency'].median():.0f} days"
        ),
        delta="Typical customer recency",
        delta_type="neutral",
    )


with rfm_summary_col2:

    kpi_card(
        label="Median Frequency",
        value=(
            f"{filtered_customers['frequency'].median():.2f}"
        ),
        delta="Typical purchase frequency",
        delta_type="neutral",
    )


with rfm_summary_col3:

    kpi_card(
        label="Median Customer Value",
        value=(
            f"{CURRENCY_SYMBOL}"
            f"{median_monetary:,.0f}"
        ),
        delta="Typical monetary value",
        delta_type="positive",
    )


# ============================================================================
# CUSTOMER VALUE RELATIONSHIP
# ============================================================================

section_header(
    title="Customer Value Relationship",
    description=(
        "Identify the relationship between purchase frequency "
        "and customer monetary value."
    ),
)


relationship_col, relationship_summary_col = st.columns(
    [1.7, 1.0],
    gap="large",
)


# ----------------------------------------------------------------------------
# Frequency vs Monetary Scatter
# ----------------------------------------------------------------------------

with relationship_col:

    scatter_chart(
        dataframe=filtered_customers,
        x="frequency",
        y="monetary",
        color="segment",
        title="Purchase Frequency vs Customer Value",
        x_title="Purchase Frequency",
        y_title="Monetary Value",
        height=420,
        opacity=0.65,
    )


# ----------------------------------------------------------------------------
# Segment Engagement Ranking
# ----------------------------------------------------------------------------

with relationship_summary_col:

    segment_engagement = (
        segment_summary[
            [
                "segment",
                "avg_frequency",
            ]
        ]
        .sort_values(
            "avg_frequency",
            ascending=True,
        )
    )


    horizontal_bar_chart(
        dataframe=segment_engagement,
        category="segment",
        value="avg_frequency",
        title="Segment Engagement",
        category_title="Segment",
        value_title="Avg Frequency",
        height=420,
        text=True,
    )


# ============================================================================
# RETENTION OPPORTUNITIES
# ============================================================================

section_header(
    title="Retention Opportunities",
    description=(
        "Prioritize customer groups based on conversion potential, "
        "retention risk, and customer value."
    ),
)


# ============================================================================
# RETENTION SEGMENT IDENTIFICATION
# ============================================================================

one_time_names = {
    "Recent One-Time Buyers",
}


risk_names = {
    "Lapsed / At Risk",
    "At Risk",
    "Lapsed",
}


one_time_count = int(
    customer_df[
        customer_df["segment"].isin(
            one_time_names
        )
    ].shape[0]
)


risk_count = int(
    customer_df[
        customer_df["segment"].isin(
            risk_names
        )
    ].shape[0]
)


high_value_count = int(
    customer_df[
        customer_df["segment"]
        .astype(str)
        .str.contains(
            "High-Value",
            case=False,
            na=False,
        )
    ].shape[0]
)


total_customer_base = int(
    customer_df[
        "customer_unique_id"
    ].nunique()
)


one_time_share = (
    one_time_count
    / total_customer_base
    if total_customer_base > 0
    else 0
)


risk_share = (
    risk_count
    / total_customer_base
    if total_customer_base > 0
    else 0
)


high_value_share = (
    high_value_count
    / total_customer_base
    if total_customer_base > 0
    else 0
)


# ============================================================================
# RETENTION VISUAL
# ============================================================================

retention_chart = pd.DataFrame(
    {
        "opportunity": [
            "One-Time Buyers",
            "At-Risk / Lapsed",
            "High-Value Customers",
        ],
        "customers": [
            one_time_count,
            risk_count,
            high_value_count,
        ],
    }
)


retention_chart = retention_chart.sort_values(
    "customers",
    ascending=True,
)


horizontal_bar_chart(
    dataframe=retention_chart,
    category="opportunity",
    value="customers",
    title="Strategic Customer Groups",
    category_title="Customer Group",
    value_title="Customers",
    height=350,
    text=True,
)


# ============================================================================
# RETENTION INSIGHTS
# ============================================================================

retention_col1, retention_col2, retention_col3 = st.columns(
    3,
    gap="medium",
)


# ----------------------------------------------------------------------------
# One-time Buyers
# ----------------------------------------------------------------------------

with retention_col1:

    insight_card(
        label="CONVERSION",
        title="One-time customer opportunity",
        description=(
            f"{one_time_count:,} customers "
            f"({one_time_share:.1%} of the customer base) "
            "are recent one-time buyers. "
            "They represent the clearest opportunity "
            "for repeat-purchase conversion."
        ),
        insight_type="warning",
    )


# ----------------------------------------------------------------------------
# At-risk Customers
# ----------------------------------------------------------------------------

with retention_col2:

    insight_card(
        label="RETENTION RISK",
        title="Lapsed customers require attention",
        description=(
            f"{risk_count:,} customers "
            f"({risk_share:.1%} of the customer base) "
            "fall into lapsed or at-risk segments."
        ),
        insight_type=(
            "danger"
            if risk_share >= 0.10
            else "warning"
        ),
    )


# ----------------------------------------------------------------------------
# High-value Customers
# ----------------------------------------------------------------------------

with retention_col3:

    insight_card(
        label="CUSTOMER VALUE",
        title="Protect high-value customers",
        description=(
            f"{high_value_count:,} customers "
            f"({high_value_share:.1%} of the customer base) "
            "are classified as high-value and should receive "
            "priority retention attention."
        ),
        insight_type="success",
    )


# ============================================================================
# SEGMENT DETAIL
# ============================================================================

section_header(
    title="Segment Performance Detail",
    description=(
        "Detailed RFM and customer-value metrics for each customer segment."
    ),
)


display_summary = segment_summary.copy()


display_summary["customer_share"] = (
    display_summary["customer_share"]
    .map(
        lambda value: f"{value:.1%}"
    )
)


display_summary["avg_recency"] = (
    display_summary["avg_recency"]
    .map(
        lambda value: f"{value:.0f} days"
    )
)


display_summary["avg_frequency"] = (
    display_summary["avg_frequency"]
    .map(
        lambda value: f"{value:.2f}"
    )
)


display_summary["avg_monetary"] = (
    display_summary["avg_monetary"]
    .map(
        lambda value: (
            f"{CURRENCY_SYMBOL}"
            f"{value:,.0f}"
        )
    )
)


display_summary["total_monetary"] = (
    display_summary["total_monetary"]
    .map(
        lambda value: (
            f"{CURRENCY_SYMBOL}"
            f"{value:,.0f}"
        )
    )
)


display_summary = display_summary.rename(
    columns={
        "segment": "Segment",
        "customers": "Customers",
        "customer_share": "Share",
        "avg_recency": "Avg Recency",
        "avg_frequency": "Avg Frequency",
        "avg_monetary": "Avg Value",
        "total_monetary": "Total Value",
    }
)


st.dataframe(
    display_summary[
        [
            "Segment",
            "Customers",
            "Share",
            "Avg Recency",
            "Avg Frequency",
            "Avg Value",
            "Total Value",
        ]
    ],
    width="stretch",
    hide_index=True,
    height=320,
)


# ============================================================================
# CUSTOMER ANALYTICS SUMMARY
# ============================================================================

section_header(
    title="Customer Analytics Summary",
    description=(
        "Key observations from the current customer segmentation analysis."
    ),
)


# ============================================================================
# SUMMARY METRICS
# ============================================================================

largest_segment_row = (
    segment_summary
    .sort_values(
        "customers",
        ascending=False,
    )
    .iloc[0]
)


largest_segment_name = (
    largest_segment_row["segment"]
)


largest_segment_size = int(
    largest_segment_row["customers"]
)


largest_segment_share = (
    largest_segment_size
    / total_customer_base
    if total_customer_base > 0
    else 0
)


highest_value_row = (
    segment_summary
    .sort_values(
        "avg_monetary",
        ascending=False,
    )
    .iloc[0]
)


highest_value_segment = (
    highest_value_row["segment"]
)


highest_value_amount = float(
    highest_value_row["avg_monetary"]
)


highest_frequency_row = (
    segment_summary
    .sort_values(
        "avg_frequency",
        ascending=False,
    )
    .iloc[0]
)


highest_frequency_segment = (
    highest_frequency_row["segment"]
)


highest_frequency_value = float(
    highest_frequency_row["avg_frequency"]
)


# ============================================================================
# SUMMARY INSIGHTS
# ============================================================================

summary_col1, summary_col2, summary_col3 = st.columns(
    3,
    gap="medium",
)


with summary_col1:

    insight_card(
        label="SEGMENT SCALE",
        title=(
            f"{largest_segment_name} is the largest segment"
        ),
        description=(
            f"It contains {largest_segment_size:,} customers, "
            f"representing {largest_segment_share:.1%} "
            "of the customer base."
        ),
        insight_type="info",
    )


with summary_col2:

    insight_card(
        label="CUSTOMER VALUE",
        title=(
            f"{highest_value_segment} has the highest value"
        ),
        description=(
            f"Average monetary value is "
            f"{CURRENCY_SYMBOL} "
            f"{highest_value_amount:,.0f} "
            "per customer."
        ),
        insight_type="success",
    )


with summary_col3:

    insight_card(
        label="ENGAGEMENT",
        title=(
            f"{highest_frequency_segment} purchases most frequently"
        ),
        description=(
            f"Average purchase frequency is "
            f"{highest_frequency_value:.2f} "
            "orders per customer."
        ),
        insight_type="info",
    )