"""
Customer Analytics
==================

Enterprise Predictive Analytics Engine

Purpose
-------
Provide a detailed analytical view of customer behavior using
the prepared RFM customer segmentation dataset.

The page covers:

- Customer KPI overview
- RFM segmentation
- Customer segment distribution
- Customer value analysis
- Frequency and monetary behavior
- Retention opportunities
- Segment-level business insights

Architecture
------------
This page uses the centralized dashboard data layer.

No CSV files are loaded directly here.
No business metrics are hardcoded.
No custom HTML is rendered directly by this page.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboards.components.alerts import insight_card
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import (
    page_header,
    section_header,
)

from dashboards.data.loader import (
    load_customer_segments,
)


# =====================================================================
# CONSTANTS
# =====================================================================

CURRENCY_SYMBOL = "R$"


# =====================================================================
# LOAD CUSTOMER DATA
# =====================================================================

# Load the prepared customer-level RFM segmentation dataset.
#
# The centralized loader handles:
# - file location
# - file validation
# - Streamlit caching
#
# This page therefore remains focused on analytics and presentation.

customer_df = load_customer_segments()


# Work on a copy so cached data is never modified.
customer_df = customer_df.copy()


# =====================================================================
# PAGE HEADER
# =====================================================================

page_header(
    title="Customer Analytics",
    description=(
        "Customer behavior, RFM segmentation, value distribution, "
        "and retention opportunities."
    ),
)


# =====================================================================
# DATA VALIDATION
# =====================================================================

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


if customer_df.empty:

    st.warning(
        "Customer segmentation data is currently unavailable."
    )

    st.stop()


# =====================================================================
# DATA PREPARATION
# =====================================================================

# Ensure the numerical RFM fields are numeric.
#
# Invalid values are converted to NaN and excluded from calculations
# where appropriate.

for column in (
    "recency",
    "frequency",
    "monetary",
):

    customer_df[column] = pd.to_numeric(
        customer_df[column],
        errors="coerce",
    )


# Remove rows without a valid customer identifier.
customer_df = customer_df.dropna(
    subset=["customer_unique_id"]
)


# Remove rows without a valid segment.
customer_df = customer_df.dropna(
    subset=["segment"]
)


# =====================================================================
# SEGMENT FILTER
# =====================================================================

section_header(
    title="Customer Analysis Controls",
    description=(
        "Focus the detailed analysis on a specific RFM customer segment."
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


# Apply the selected segment filter.
if selected_segment == "All Segments":

    filtered_customers = customer_df.copy()

else:

    filtered_customers = customer_df[
        customer_df["segment"].astype(str)
        == selected_segment
    ].copy()


# =====================================================================
# CUSTOMER KPI OVERVIEW
# =====================================================================

section_header(
    title="Customer KPI Overview",
    description=(
        "Core customer metrics calculated from the RFM customer-level data."
    ),
)


# ---------------------------------------------------------------------
# KPI calculations
# ---------------------------------------------------------------------

total_customers = int(
    filtered_customers["customer_unique_id"].nunique()
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
    filtered_customers["frequency"].mean()
)


average_monetary = (
    filtered_customers["monetary"].mean()
)


average_recency = (
    filtered_customers["recency"].mean()
)


# =====================================================================
# KPI CARDS
# =====================================================================

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)


# ---------------------------------------------------------------------
# Total Customers
# ---------------------------------------------------------------------

with kpi_col1:

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


# ---------------------------------------------------------------------
# Repeat Customer Rate
# ---------------------------------------------------------------------

with kpi_col2:

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


# ---------------------------------------------------------------------
# Average Purchase Frequency
# ---------------------------------------------------------------------

with kpi_col3:

    kpi_card(
        label="Avg. Purchase Frequency",
        value=f"{average_frequency:.2f}",
        delta="Orders per customer",
        delta_type="neutral",
    )


# ---------------------------------------------------------------------
# Average Customer Value
# ---------------------------------------------------------------------

with kpi_col4:

    kpi_card(
        label="Avg. Customer Value",
        value=(
            f"{CURRENCY_SYMBOL}"
            f"{average_monetary:,.0f}"
        ),
        delta="Average RFM monetary value",
        delta_type="positive",
    )


# =====================================================================
# CUSTOMER SEGMENTATION
# =====================================================================

section_header(
    title="Customer Segmentation",
    description=(
        "Distribution and economic value of the project's RFM customer segments."
    ),
)


segment_chart_col, value_chart_col = st.columns(
    [1.45, 1],
    gap="large",
)


# =====================================================================
# SEGMENT DISTRIBUTION
# =====================================================================

with segment_chart_col:

    segment_counts = (
        customer_df["segment"]
        .value_counts()
        .reset_index()
    )


    segment_counts.columns = [
        "segment",
        "customers",
    ]


    segment_counts = (
        segment_counts
        .sort_values(
            "customers",
            ascending=True,
        )
    )


    segment_counts["share"] = (
        segment_counts["customers"]
        / segment_counts["customers"].sum()
    )


    figure = px.bar(
        segment_counts,
        x="customers",
        y="segment",
        orientation="h",
        text="customers",
    )


    figure.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        marker_color="#2563EB",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Customers: %{x:,}<br>"
            "<extra></extra>"
        ),
    )


    figure.update_layout(
        title=dict(
            text="Customer Distribution by Segment",
            x=0,
            xanchor="left",
            font=dict(
                size=16,
                color="#111827",
            ),
        ),
        height=360,
        margin=dict(
            l=5,
            r=35,
            t=45,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=(
                "Inter, -apple-system, "
                "BlinkMacSystemFont, Segoe UI, sans-serif"
            ),
            color="#64748B",
        ),
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="#EEF2F7",
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            showline=False,
        ),
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================================
# AVERAGE CUSTOMER VALUE BY SEGMENT
# =====================================================================

with value_chart_col:

    segment_value = (
        customer_df
        .groupby("segment", as_index=False)
        .agg(
            average_monetary=(
                "monetary",
                "mean",
            )
        )
        .sort_values(
            "average_monetary",
            ascending=True,
        )
    )


    figure = px.bar(
        segment_value,
        x="average_monetary",
        y="segment",
        orientation="h",
        text="average_monetary",
    )


    figure.update_traces(
        texttemplate="R$ %{text:,.0f}",
        textposition="outside",
        marker_color="#0F766E",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Average value: R$%{x:,.0f}"
            "<extra></extra>"
        ),
    )


    figure.update_layout(
        title=dict(
            text="Average Customer Value by Segment",
            x=0,
            xanchor="left",
            font=dict(
                size=16,
                color="#111827",
            ),
        ),
        height=360,
        margin=dict(
            l=5,
            r=45,
            t=45,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=(
                "Inter, -apple-system, "
                "BlinkMacSystemFont, Segoe UI, sans-serif"
            ),
            color="#64748B",
        ),
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="#EEF2F7",
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            showline=False,
        ),
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================================
# RFM ANALYSIS
# =====================================================================

section_header(
    title="RFM Analysis",
    description=(
        "Understand customer recency, purchase frequency, and monetary value."
    ),
)


rfm_col1, rfm_col2, rfm_col3 = st.columns(
    3,
    gap="medium",
)


# =====================================================================
# RECENCY DISTRIBUTION
# =====================================================================

with rfm_col1:

    figure = px.histogram(
        filtered_customers,
        x="recency",
        nbins=30,
    )


    figure.update_traces(
        marker_color="#2563EB",
        hovertemplate=(
            "Recency: %{x}<br>"
            "Customers: %{y:,}"
            "<extra></extra>"
        ),
    )


    figure.update_layout(
        title="Recency Distribution",
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=45,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#64748B",
        ),
        xaxis_title="Days Since Last Purchase",
        yaxis_title="Customers",
        bargap=0.08,
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================================
# FREQUENCY DISTRIBUTION
# =====================================================================

with rfm_col2:

    figure = px.histogram(
        filtered_customers,
        x="frequency",
        nbins=20,
    )


    figure.update_traces(
        marker_color="#7C3AED",
        hovertemplate=(
            "Frequency: %{x}<br>"
            "Customers: %{y:,}"
            "<extra></extra>"
        ),
    )


    figure.update_layout(
        title="Purchase Frequency",
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=45,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#64748B",
        ),
        xaxis_title="Orders per Customer",
        yaxis_title="Customers",
        bargap=0.08,
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================================
# MONETARY DISTRIBUTION
# =====================================================================

with rfm_col3:

    figure = px.histogram(
        filtered_customers,
        x="monetary",
        nbins=30,
    )


    figure.update_traces(
        marker_color="#0F766E",
        hovertemplate=(
            "Monetary: R$%{x:,.0f}<br>"
            "Customers: %{y:,}"
            "<extra></extra>"
        ),
    )


    figure.update_layout(
        title="Monetary Value Distribution",
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=45,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#64748B",
        ),
        xaxis_title="Customer Monetary Value (R$)",
        yaxis_title="Customers",
        bargap=0.08,
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================================
# CUSTOMER VALUE BEHAVIOR
# =====================================================================

section_header(
    title="Customer Value Behavior",
    description=(
        "Explore how purchase frequency relates to customer monetary value."
    ),
)


value_behavior_col, summary_col = st.columns(
    [1.7, 1],
    gap="large",
)


# =====================================================================
# FREQUENCY VS MONETARY VALUE
# =====================================================================

with value_behavior_col:

    scatter_data = filtered_customers.dropna(
        subset=[
            "frequency",
            "monetary",
            "segment",
        ]
    ).copy()


    figure = px.scatter(
        scatter_data,
        x="frequency",
        y="monetary",
        color="segment",
        hover_data={
            "frequency": True,
            "monetary": ":,.0f",
            "segment": True,
        },
        opacity=0.65,
    )


    figure.update_traces(
        marker=dict(
            size=7,
        ),
    )


    figure.update_layout(
        title=dict(
            text="Purchase Frequency vs Customer Value",
            x=0,
            xanchor="left",
            font=dict(
                size=16,
                color="#111827",
            ),
        ),
        height=390,
        margin=dict(
            l=5,
            r=5,
            t=45,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=(
                "Inter, -apple-system, "
                "BlinkMacSystemFont, Segoe UI, sans-serif"
            ),
            color="#64748B",
        ),
        xaxis=dict(
            title="Purchase Frequency",
            showgrid=True,
            gridcolor="#EEF2F7",
            zeroline=False,
        ),
        yaxis=dict(
            title="Monetary Value (R$)",
            showgrid=True,
            gridcolor="#EEF2F7",
            zeroline=False,
        ),
        legend=dict(
            title="Segment",
            font=dict(size=10),
        ),
    )


    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =====================================================================
# CUSTOMER SEGMENT PERFORMANCE SUMMARY
# =====================================================================

with summary_col:

    st.markdown("### Segment Performance")

    st.caption(
        "Business-level comparison of customer segments."
    )


    segment_summary = (
        customer_df
        .groupby("segment", as_index=False)
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


    display_summary = segment_summary.copy()


    display_summary["customer_share"] = (
        display_summary["customer_share"]
        .map(lambda value: f"{value:.1%}")
    )


    display_summary["avg_recency"] = (
        display_summary["avg_recency"]
        .map(lambda value: f"{value:.0f}")
    )


    display_summary["avg_frequency"] = (
        display_summary["avg_frequency"]
        .map(lambda value: f"{value:.2f}")
    )


    display_summary["avg_monetary"] = (
        display_summary["avg_monetary"]
        .map(
            lambda value: f"R$ {value:,.0f}"
        )
    )


    display_summary["total_monetary"] = (
        display_summary["total_monetary"]
        .map(
            lambda value: f"R$ {value:,.0f}"
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
        use_container_width=True,
        hide_index=True,
        height=390,
    )


# =====================================================================
# RETENTION OPPORTUNITY
# =====================================================================

section_header(
    title="Retention Opportunities",
    description=(
        "Identify customer groups that require attention or represent "
        "high-value retention opportunities."
    ),
)


# ---------------------------------------------------------------------
# Identify strategic customer groups
# ---------------------------------------------------------------------

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
        customer_df["segment"].isin(one_time_names)
    ].shape[0]
)


risk_count = int(
    customer_df[
        customer_df["segment"].isin(risk_names)
    ].shape[0]
)


high_value_count = int(
    customer_df[
        customer_df["segment"].astype(str)
        .str.contains(
            "High-Value",
            case=False,
            na=False,
        )
    ].shape[0]
)


total_customer_base = int(
    customer_df["customer_unique_id"].nunique()
)


one_time_share = (
    one_time_count / total_customer_base
    if total_customer_base > 0
    else 0
)


risk_share = (
    risk_count / total_customer_base
    if total_customer_base > 0
    else 0
)


high_value_share = (
    high_value_count / total_customer_base
    if total_customer_base > 0
    else 0
)


retention_col1, retention_col2, retention_col3 = st.columns(
    3,
    gap="medium",
)


# ---------------------------------------------------------------------
# One-time buyers
# ---------------------------------------------------------------------

with retention_col1:

    insight_card(
        label="CONVERSION",
        title="One-time customer opportunity",
        description=(
            f"{one_time_count:,} customers "
            f"({one_time_share:.1%} of the customer base) "
            "are classified as recent one-time buyers. "
            "They represent the clearest opportunity for "
            "repeat-purchase conversion."
        ),
        insight_type="warning",
    )


# ---------------------------------------------------------------------
# At-risk customers
# ---------------------------------------------------------------------

with retention_col2:

    insight_card(
        label="RETENTION RISK",
        title="Lapsed customers require attention",
        description=(
            f"{risk_count:,} customers "
            f"({risk_share:.1%} of the customer base) "
            "fall into the lapsed or at-risk segment."
        ),
        insight_type=(
            "danger"
            if risk_share >= 0.10
            else "warning"
        ),
    )


# ---------------------------------------------------------------------
# High-value customers
# ---------------------------------------------------------------------

with retention_col3:

    insight_card(
        label="CUSTOMER VALUE",
        title="Protect high-value customers",
        description=(
            f"{high_value_count:,} customers "
            f"({high_value_share:.1%} of the customer base) "
            "are classified as high-value customers and "
            "should receive priority retention attention."
        ),
        insight_type="success",
    )


# =====================================================================
# CUSTOMER ANALYTICS SUMMARY
# =====================================================================

section_header(
    title="Customer Analytics Summary",
    description=(
        "Key observations from the current customer segmentation analysis."
    ),
)


# ---------------------------------------------------------------------
# Find largest segment
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Find highest-value segment
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Find most frequent segment
# ---------------------------------------------------------------------

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


summary_col1, summary_col2, summary_col3 = st.columns(
    3,
    gap="medium",
)


# ---------------------------------------------------------------------
# Largest segment insight
# ---------------------------------------------------------------------

with summary_col1:

    insight_card(
        label="SEGMENT SCALE",
        title=f"{largest_segment_name} is the largest segment",
        description=(
            f"It contains {largest_segment_size:,} customers, "
            f"representing {largest_segment_share:.1%} of the "
            "customer base."
        ),
        insight_type="info",
    )


# ---------------------------------------------------------------------
# Highest-value segment insight
# ---------------------------------------------------------------------

with summary_col2:

    insight_card(
        label="CUSTOMER VALUE",
        title=f"{highest_value_segment} has the highest average value",
        description=(
            f"Average monetary value is "
            f"R$ {highest_value_amount:,.0f} per customer."
        ),
        insight_type="success",
    )


# ---------------------------------------------------------------------
# Highest-frequency segment insight
# ---------------------------------------------------------------------

with summary_col3:

    insight_card(
        label="ENGAGEMENT",
        title=f"{highest_frequency_segment} purchases most frequently",
        description=(
            f"Average purchase frequency is "
            f"{highest_frequency_value:.2f} orders per customer."
        ),
        insight_type="info",
    )