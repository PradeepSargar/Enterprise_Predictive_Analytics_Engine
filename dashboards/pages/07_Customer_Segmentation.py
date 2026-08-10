"""
Customer Segmentation Dashboard.

This page presents customer-level segmentation using the existing
RFM and clustering outputs.

Responsibilities
----------------
1. Load the prepared customer segmentation dataset.
2. Use the transformation layer to create dashboard-ready metrics.
3. Present segment distribution and business performance.
4. Visualize RFM behavior using reusable chart components.
5. Present a detailed segment-performance table.

Business logic remains inside dashboards.data.transformations.
Visualization logic remains inside dashboards.components.charts.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

from dashboards.components.charts import (
    bar_chart,
    donut_chart,
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
# TRANSFORMATION LAYER
# ============================================================================

from dashboards.data.transformations import (
    calculate_customer_segment_summary,
    calculate_rfm_summary,
    calculate_segment_performance,
)


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="Customer Segmentation",
    description=(
        "Understand customer groups through RFM behavior, "
        "segment size, and monetary value."
    ),
)


# ============================================================================
# LOAD CUSTOMER SEGMENTATION DATA
# ============================================================================

try:

    customer_segments = load_customer_segments()

except FileNotFoundError as exc:

    st.error(
        "Customer segmentation data could not be loaded."
    )

    st.caption(str(exc))

    st.stop()

except Exception as exc:

    st.error(
        "An unexpected error occurred while loading "
        "customer segmentation data."
    )

    st.caption(str(exc))

    st.stop()


# ============================================================================
# DATA VALIDATION
# ============================================================================

if customer_segments is None or customer_segments.empty:

    st.warning(
        "Customer segmentation data is currently unavailable."
    )

    st.stop()


required_columns = {
    "customer_unique_id",
    "recency",
    "frequency",
    "monetary",
    "segment",
}


missing_columns = (
    required_columns
    - set(customer_segments.columns)
)


if missing_columns:

    st.error(
        "Customer segmentation data is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )

    st.stop()


# ============================================================================
# PREPARE NUMERIC DATA
# ============================================================================

# Work on a copy so the dataframe returned by the cached loader
# is never modified directly.

customer_segments = customer_segments.copy()


numeric_columns = [
    "recency",
    "frequency",
    "monetary",
]


for column in numeric_columns:

    customer_segments[column] = pd.to_numeric(
        customer_segments[column],
        errors="coerce",
    )


# Remove invalid records that cannot participate in RFM analysis.

customer_segments = customer_segments.dropna(
    subset=[
        "customer_unique_id",
        "segment",
        "recency",
        "frequency",
        "monetary",
    ]
)


if customer_segments.empty:

    st.warning(
        "No valid customer records are available after data validation."
    )

    st.stop()


# ============================================================================
# BUSINESS TRANSFORMATIONS
# ============================================================================

try:

    segment_summary = calculate_customer_segment_summary(
        customer_segments
    )

    segment_performance = calculate_segment_performance(
        customer_segments
    )

    rfm_summary = calculate_rfm_summary(
        customer_segments
    )

except Exception as exc:

    st.error(
        "Customer segmentation metrics could not be calculated."
    )

    st.caption(str(exc))

    st.stop()


# ============================================================================
# NORMALIZE SEGMENT SUMMARY
# ============================================================================

# Some transformation implementations may return the percentage
# under the name "percentage". Normalize it to "customer_share".

if (
    "percentage" in segment_summary.columns
    and "customer_share" not in segment_summary.columns
):

    segment_summary = segment_summary.rename(
        columns={
            "percentage": "customer_share"
        }
    )


# ============================================================================
# KPI CALCULATIONS
# ============================================================================

total_customers = (
    customer_segments["customer_unique_id"]
    .nunique()
)


total_segments = (
    customer_segments["segment"]
    .nunique()
)


average_monetary = (
    customer_segments["monetary"]
    .mean()
)


average_frequency = (
    customer_segments["frequency"]
    .mean()
)


# ============================================================================
# SEGMENTATION OVERVIEW
# ============================================================================

section_header(
    title="Segmentation Overview",
    description=(
        "High-level customer segmentation metrics."
    ),
)


kpi_columns = st.columns(
    4,
    gap="large",
)


with kpi_columns[0]:

    kpi_card(
        label="Total Customers",
        value=f"{total_customers:,}",
        delta="Unique customers",
        delta_type="neutral",
    )


with kpi_columns[1]:

    kpi_card(
        label="Customer Segments",
        value=f"{total_segments:,}",
        delta="Identified groups",
        delta_type="neutral",
    )


with kpi_columns[2]:

    kpi_card(
        label="Avg Monetary Value",
        value=f"R${average_monetary:,.2f}",
        delta="Average customer value",
        delta_type="positive",
    )


with kpi_columns[3]:

    kpi_card(
        label="Avg Purchase Frequency",
        value=f"{average_frequency:.2f}",
        delta="Purchases per customer",
        delta_type="neutral",
    )


# ============================================================================
# SEGMENT DISTRIBUTION
# ============================================================================

section_header(
    title="Segment Distribution",
    description=(
        "Customer concentration across the identified behavioral segments."
    ),
)


distribution_columns = st.columns(
    2,
    gap="large",
)


with distribution_columns[0]:

    donut_chart(
        dataframe=segment_summary,
        names="segment",
        values="customers",
        title="Customer Distribution by Segment",
        height=380,
    )


with distribution_columns[1]:

    bar_chart(
        dataframe=segment_summary,
        x="segment",
        y="customers",
        title="Customers by Segment",
        x_title="Customer Segment",
        y_title="Customers",
        height=380,
    )


# ============================================================================
# SEGMENT PERFORMANCE
# ============================================================================

section_header(
    title="Segment Performance",
    description=(
        "Compare customer value and behavioral characteristics "
        "across segments."
    ),
)


performance_columns = st.columns(
    2,
    gap="large",
)


with performance_columns[0]:

    bar_chart(
        dataframe=segment_performance,
        x="segment",
        y="avg_monetary",
        title="Average Monetary Value by Segment",
        x_title="Customer Segment",
        y_title="Average Monetary Value",
        height=380,
    )


with performance_columns[1]:

    bar_chart(
        dataframe=segment_performance,
        x="segment",
        y="total_monetary",
        title="Total Monetary Value by Segment",
        x_title="Customer Segment",
        y_title="Total Monetary Value",
        height=380,
    )


# ============================================================================
# RFM BEHAVIOR
# ============================================================================

section_header(
    title="RFM Behavioral Analysis",
    description=(
        "Overall customer behavior across recency, frequency, "
        "and monetary value."
    ),
)


rfm_columns = st.columns(
    3,
    gap="large",
)


with rfm_columns[0]:

    kpi_card(
        label="Median Recency",
        value=f"{rfm_summary['recency_median']:.1f}",
        delta="Days since purchase",
        delta_type="neutral",
    )


with rfm_columns[1]:

    kpi_card(
        label="Median Frequency",
        value=f"{rfm_summary['frequency_median']:.1f}",
        delta="Purchases per customer",
        delta_type="neutral",
    )


with rfm_columns[2]:

    kpi_card(
        label="Median Monetary",
        value=f"R${rfm_summary['monetary_median']:,.2f}",
        delta="Customer monetary value",
        delta_type="positive",
    )


# ============================================================================
# CUSTOMER VALUE RELATIONSHIP
# ============================================================================

section_header(
    title="Customer Value Relationship",
    description=(
        "Relationship between purchase frequency and monetary value "
        "across customer segments."
    ),
)


scatter_chart(
    dataframe=customer_segments,
    x="frequency",
    y="monetary",
    color="segment",
    title="Purchase Frequency vs Monetary Value",
    x_title="Purchase Frequency",
    y_title="Monetary Value",
    height=450,
)


# ============================================================================
# SEGMENT PERFORMANCE DETAIL
# ============================================================================

section_header(
    title="Segment Performance Detail",
    description=(
        "Detailed customer volume and RFM metrics for each segment."
    ),
)


# ============================================================================
# PREPARE TABLE DATA
# ============================================================================

# Create a dedicated presentation dataframe.
# This does not modify the original transformation output.

display_df = segment_performance[
    [
        "segment",
        "customers",
        "customer_share",
        "avg_recency",
        "avg_frequency",
        "avg_monetary",
        "total_monetary",
    ]
].copy()


# ============================================================================
# RENAME TABLE COLUMNS
# ============================================================================

display_df = display_df.rename(
    columns={
        "segment": "Customer Segment",
        "customers": "Customers",
        "customer_share": "Customer Share (%)",
        "avg_recency": "Avg Recency (Days)",
        "avg_frequency": "Avg Frequency",
        "avg_monetary": "Avg Monetary Value",
        "total_monetary": "Total Monetary Value",
    }
)


# ============================================================================
# FORMAT CUSTOMER SHARE
# ============================================================================

# customer_share is stored as a decimal ratio.
#
# Example:
# 0.555 -> 55.5
#
# The NumberColumn below adds the % symbol.

display_df["Customer Share (%)"] = (
    display_df["Customer Share (%)"] * 100
)


# ============================================================================
# PROFESSIONAL NATIVE STREAMLIT TABLE
# ============================================================================

# IMPORTANT:
#
# We intentionally use Streamlit's native dataframe renderer.
#
# There is NO custom HTML table here.
# There is NO <table>, <thead>, <tbody>, <tr>, or <td>.
#
# This prevents the raw HTML problem that appeared previously.

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
    height=250,
    column_config={

        "Customer Segment": st.column_config.TextColumn(
            "Customer Segment",
            width="large",
        ),

        "Customers": st.column_config.NumberColumn(
            "Customers",
            format="%,d",
            width="medium",
        ),

        "Customer Share (%)": st.column_config.NumberColumn(
            "Customer Share (%)",
            format="%.1f%%",
            width="medium",
        ),

        "Avg Recency (Days)": st.column_config.NumberColumn(
            "Avg Recency (Days)",
            format="%.1f",
            width="medium",
        ),

        "Avg Frequency": st.column_config.NumberColumn(
            "Avg Frequency",
            format="%.2f",
            width="medium",
        ),

        "Avg Monetary Value": st.column_config.NumberColumn(
            "Avg Monetary Value",
            format="R$%.2f",
            width="medium",
        ),

        "Total Monetary Value": st.column_config.NumberColumn(
            "Total Monetary Value",
            format="R$%.2f",
            width="large",
        ),
    },
)