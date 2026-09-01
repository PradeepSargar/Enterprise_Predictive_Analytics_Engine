"""
Customer Segmentation Dashboard.
================================
Enterprise Predictive Analytics Engine

This page presents customer-level RFM behavioral segmentation and clustering intelligence.

Responsibilities:
1. Load prepared customer segmentation dataset.
2. Calculate segment summaries, performance metrics, and RFM medians.
3. Visualize customer cluster mix and gross monetary contribution.
4. Profile behavioral relationships and segment strategy playbooks.
5. Export detailed segment performance table.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboards.components.alerts import insight_card
from dashboards.components.charts import bar_chart, donut_chart, scatter_chart
from dashboards.components.containers import panel
from dashboards.components.exports import csv_download, excel_download
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import page_header, section_header
from dashboards.components.tables import render_styled_table
from dashboards.data.loader import load_customer_segments
from dashboards.data.transformations import (
    calculate_customer_segment_summary,
    calculate_rfm_summary,
    calculate_segment_performance,
)
from dashboards.utils.constants import CURRENCY_SYMBOL
from dashboards.utils.html import render_html

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Customer Segmentation",
    description=(
        "Understand customer groups through RFM behavior, "
        "cluster size, revenue contribution, and strategic value."
    ),
    status="RFM & CLUSTER INTELLIGENCE",
)

render_html(
    """
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #1B4332 0%, #143628 50%, #0F281E 100%);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(15, 40, 30, 0.20);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.10);
    ">
        <div style="
            position: absolute;
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(244, 162, 97, 0.22) 0%, rgba(244, 162, 97, 0) 70%);
            top: -70px;
            right: 50px;
            pointer-events: none;
        "></div>
        <div style="
            position: absolute;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(82, 183, 136, 0.18) 0%, rgba(82, 183, 136, 0) 70%);
            bottom: -50px;
            right: -20px;
            pointer-events: none;
        "></div>

        <div style="position: relative; z-index: 2; max-width: 820px;">
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 0.25rem 0.6rem;
                border-radius: 999px;
                background: rgba(244, 162, 97, 0.18);
                border: 1px solid rgba(244, 162, 97, 0.35);
                font-size: 8.5px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
                color: #F4A261;
            ">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#F4A261;"></span>
                BEHAVIORAL RFM & CLUSTERING
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Cohort Profiling & Strategic Revenue Allocation
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F1FAEE;">
                Evaluate Brazilian e-commerce buyer distributions across Recency (inactivity decay),
                Frequency (lifetime orders), and Monetary Value (cumulative GMV) to tailor marketing interventions.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# LOAD DATA & VALIDATE
# ============================================================================

try:
    customer_segments = load_customer_segments()
except Exception as exc:
    st.error("Customer segmentation data could not be loaded.")
    st.caption(str(exc))
    st.stop()

if customer_segments is None or customer_segments.empty:
    st.warning("Customer segmentation data is currently unavailable.")
    st.stop()

customer_segments = customer_segments.copy()

for col in ("recency", "frequency", "monetary"):
    if col in customer_segments.columns:
        customer_segments[col] = pd.to_numeric(customer_segments[col], errors="coerce")

customer_segments = customer_segments.dropna(
    subset=["customer_unique_id", "segment", "recency", "frequency", "monetary"]
)

# ============================================================================
# TRANSFORMATIONS
# ============================================================================

segment_summary = calculate_customer_segment_summary(customer_segments)
segment_performance = calculate_segment_performance(customer_segments)
rfm_summary = calculate_rfm_summary(customer_segments)

if "percentage" in segment_summary.columns and "customer_share" not in segment_summary.columns:
    segment_summary = segment_summary.rename(columns={"percentage": "customer_share"})

total_customers = customer_segments["customer_unique_id"].nunique()
total_segments = customer_segments["segment"].nunique()
average_monetary = float(customer_segments["monetary"].mean())
average_frequency = float(customer_segments["frequency"].mean())

# ============================================================================
# SEGMENTATION OVERVIEW KPIs
# ============================================================================

section_header(
    title="Segmentation Scorecard",
    description="High-level customer population, cluster cardinality, and average financial spend.",
)

kpi_columns = st.columns(4, gap="large")

with kpi_columns[0]:
    kpi_card(
        label="Total Customers",
        value=f"{total_customers:,}",
        delta="Unique customer IDs",
        delta_type="neutral",
    )

with kpi_columns[1]:
    kpi_card(
        label="Identified Clusters",
        value=f"{total_segments:,}",
        delta="Behavioral segments",
        delta_type="neutral",
    )

with kpi_columns[2]:
    kpi_card(
        label="Avg Customer Value",
        value=f"R$ {average_monetary:,.2f}",
        delta="Mean lifetime spend",
        delta_type="positive",
    )

with kpi_columns[3]:
    kpi_card(
        label="Avg Purchase Frequency",
        value=f"{average_frequency:.2f}",
        delta="Orders per customer",
        delta_type="neutral",
    )

# ============================================================================
# SEGMENT DISTRIBUTION & SCALE
# ============================================================================

section_header(
    title="Segment Distribution & Volume Mix",
    description="Customer concentration and population scale across identified behavioral clusters.",
)

dist_col1, dist_col2 = st.columns(2, gap="large")

with dist_col1:
    with panel(
        title="Customer Distribution by Segment",
        description="Share of marketplace buyers categorized in each cluster.",
        badge="CLUSTER MIX",
        footer_insight="One-Time buyers account for 55.5% of total marketplace customer profiles.",
    ):
        donut_chart(
            dataframe=segment_summary,
            names="segment",
            values="customers",
            title=None,
            height=370,
        )

with dist_col2:
    with panel(
        title="Customer Volume by Segment",
        description="Total unique buyers per behavioral group.",
        badge="HEADCOUNT",
        footer_insight="Lapsed / At Risk cohort represents 34.2k customers needing retention campaigns.",
    ):
        bar_chart(
            dataframe=segment_summary,
            x="segment",
            y="customers",
            title=None,
            x_title="Segment",
            y_title="Customers",
            height=370,
        )

# ============================================================================
# SEGMENT PERFORMANCE & GMV CONTRIBUTION
# ============================================================================

section_header(
    title="Segment Financial Performance",
    description="Compare average monetary value and total GMV contribution across customer segments.",
)

perf_col1, perf_col2 = st.columns(2, gap="large")

with perf_col1:
    with panel(
        title="Average Monetary Spend (R$)",
        description="Mean expenditure per buyer across segments.",
        badge="PER BUYER GMV",
        footer_insight="High-Value Outliers average R$1,263/buyer, 7.6x higher than standard buyers.",
    ):
        bar_chart(
            dataframe=segment_performance,
            x="segment",
            y="avg_monetary",
            title=None,
            x_title="Segment",
            y_title="Avg Spend (R$)",
            height=370,
        )

with perf_col2:
    with panel(
        title="Total Cumulative GMV (R$)",
        description="Aggregate revenue generated by each customer cohort.",
        badge="TOTAL CONTRIBUTION",
        footer_insight="One-Time Buyers generated R$7.8M in aggregate GMV.",
    ):
        bar_chart(
            dataframe=segment_performance,
            x="segment",
            y="total_monetary",
            title=None,
            x_title="Segment",
            y_title="Total GMV (R$)",
            height=370,
        )

# ============================================================================
# RFM BEHAVIORAL MEDIANS & VALUE RELATIONSHIP
# ============================================================================

section_header(
    title="RFM Behavioral Medians & Relationship Mapping",
    description="Examine median RFM values and scatter correlation between frequency and monetary spend.",
)

rfm_cols = st.columns(3, gap="medium")

with rfm_cols[0]:
    kpi_card(
        label="Median Inactivity",
        value=f"{rfm_summary['recency_median']:.0f} days",
        delta="Days since last purchase",
        delta_type="neutral",
    )

with rfm_cols[1]:
    kpi_card(
        label="Median Frequency",
        value=f"{rfm_summary['frequency_median']:.2f}",
        delta="Orders per customer",
        delta_type="neutral",
    )

with rfm_cols[2]:
    kpi_card(
        label="Median Spend",
        value=f"R$ {rfm_summary['monetary_median']:,.2f}",
        delta="Customer spend median",
        delta_type="positive",
    )

render_html("<div style='height: 12px;'></div>")

with panel(
    title="Frequency vs Customer Monetary Spend Scatter",
    description="Multivariate mapping highlighting high-value outliers and repeat customer clusters.",
):
    scatter_chart(
        dataframe=customer_segments,
        x="frequency",
        y="monetary",
        color="segment",
        title=None,
        x_title="Lifetime Orders",
        y_title="Monetary Value (R$)",
        height=420,
    )

# ============================================================================
# SEGMENT PERFORMANCE TABLE & EXPORTS
# ============================================================================

section_header(
    title="Segment Performance Master Table",
    description="Granular metrics across all behavioral clusters formatted in Brazilian Real (R$).",
)

with panel(
    title="Customer Segment Breakdown",
    description="Detailed table showing buyer counts, marketplace share, and average RFM metrics.",
):
    display_df = segment_performance.copy()
    display_df = display_df.rename(
        columns={
            "segment": "Customer Segment",
            "customers": "Customers",
            "customer_share": "Marketplace Share",
            "avg_recency": "Avg Recency (Days)",
            "avg_frequency": "Avg Frequency",
            "avg_monetary": "Avg Value (R$)",
            "total_monetary": "Total Value (R$)",
        }
    )

    # Convert share to percentage if needed
    if display_df["Marketplace Share"].max() <= 1.0:
        display_df["Marketplace Share"] = display_df["Marketplace Share"] * 100.0

    render_styled_table(
        display_df,
        column_formats={
            "Customers": "{:,.0f}",
            "Marketplace Share": "{:.1f}%",
            "Avg Recency (Days)": "{:.0f} days",
            "Avg Frequency": "{:.2f}",
            "Avg Value (R$)": "R$ {:,.2f}",
            "Total Value (R$)": "R$ {:,.2f}",
        },
        progress_columns=["Marketplace Share"],
    )

    col_exp1, col_exp2, col_sp = st.columns([1, 1, 2], gap="small")
    with col_exp1:
        csv_download(display_df, filename="segment_performance_summary.csv", key="csv_seg_perf")
    with col_exp2:
        excel_download(display_df, filename="segment_performance_summary.xlsx", key="excel_seg_perf")