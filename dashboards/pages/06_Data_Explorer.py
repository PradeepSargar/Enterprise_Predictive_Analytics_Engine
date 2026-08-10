"""
Data Explorer Dashboard.
========================
Enterprise Predictive Analytics Engine

This page provides an interactive data catalog, quality inspection workspace,
column profiler, and filterable data preview for the processed master dataset.

Responsibilities:
1. Load processed master records through the centralized loader.
2. Provide dataset-level telemetry (rows, columns, unique orders/customers, memory).
3. Display data quality completeness and missingness audit.
4. Interactive column schema & type profiler.
5. Column distribution inspector.
6. Searchable data preview with CSV/Excel export.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboards.components.alerts import insight_card
from dashboards.components.charts import bar_chart, histogram
from dashboards.components.containers import panel
from dashboards.components.exports import csv_download, excel_download
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import page_header, section_header
from dashboards.data.loader import load_master_data
from dashboards.utils.constants import CHART_PALETTE, PRIMARY_COLOR, TEXT_COLOR
from dashboards.utils.html import render_html

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Data Explorer",
    description=(
        "Explore the processed master e-commerce dataset, inspect schemas, "
        "evaluate data quality, and filter records interactively."
    ),
    status="DATA CATALOG & SCHEMA",
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
                DATA GOVERNANCE & SCHEMA PROFILER
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Master Dataset Catalog & Quality Inspection Workspace
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F0F9FF;">
                Verify dimensional structures, cardinality distributions, null-value completeness,
                and underlying records powering the predictive modeling and forecasting pipelines.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# LOAD MASTER DATA
# ============================================================================

try:
    master_df = load_master_data()
except Exception as exc:
    st.error("The processed master dataset could not be loaded.")
    st.caption(str(exc))
    st.stop()

if master_df is None or master_df.empty:
    st.warning("The master dataset is currently empty.")
    st.stop()

total_rows = len(master_df)
total_columns = len(master_df.columns)
total_orders = master_df["order_id"].nunique() if "order_id" in master_df.columns else 0
total_customers = master_df["customer_unique_id"].nunique() if "customer_unique_id" in master_df.columns else 0

# ============================================================================
# DATASET OVERVIEW
# ============================================================================

section_header(
    title="Dataset Telemetry & Volume Overview",
    description="High-level cardinality and scale statistics for the processed master table.",
)

kpi_columns = st.columns(4, gap="large")

with kpi_columns[0]:
    kpi_card(
        label="Total Master Records",
        value=f"{total_rows:,}",
        delta="Order item observations",
        delta_type="neutral",
    )

with kpi_columns[1]:
    kpi_card(
        label="Schema Attributes",
        value=f"{total_columns:,}",
        delta="Cleaned feature columns",
        delta_type="neutral",
    )

with kpi_columns[2]:
    kpi_card(
        label="Unique Orders",
        value=f"{total_orders:,}",
        delta="E-commerce transactions",
        delta_type="neutral",
    )

with kpi_columns[3]:
    kpi_card(
        label="Unique Buyers",
        value=f"{total_customers:,}",
        delta="Customer IDs",
        delta_type="neutral",
    )

# ============================================================================
# DATA QUALITY
# ============================================================================

section_header(
    title="Data Quality & Integrity Audit",
    description="Review cell-level completeness, missingness ratios, and record consistency.",
)

missing_cells = int(master_df.isna().sum().sum())
total_cells = master_df.shape[0] * master_df.shape[1]
missing_percentage = (missing_cells / total_cells) * 100 if total_cells > 0 else 0.0
duplicate_rows = int(master_df.duplicated().sum())
complete_rows = int(master_df.notna().all(axis=1).sum())
completeness_percentage = (complete_rows / total_rows) * 100 if total_rows > 0 else 0.0

qual_col1, qual_col2, qual_col3 = st.columns(3, gap="medium")

with qual_col1:
    kpi_card(
        label="Missing Data Ratio",
        value=f"{missing_percentage:.2f}%",
        delta=f"{missing_cells:,} missing cells",
        delta_type="positive" if missing_percentage < 1.0 else "warning",
    )

with qual_col2:
    kpi_card(
        label="Duplicate Records",
        value=f"{duplicate_rows:,}",
        delta="Exact duplicate rows",
        delta_type="positive" if duplicate_rows == 0 else "negative",
    )

with qual_col3:
    kpi_card(
        label="Complete Rows Ratio",
        value=f"{completeness_percentage:.1f}%",
        delta=f"{complete_rows:,} complete rows",
        delta_type="positive",
    )

# ============================================================================
# COLUMN SCHEMA PROFILER
# ============================================================================

section_header(
    title="Column Schema & Attribute Profiler",
    description="Inspect data types, non-null counts, missingness percentage, and unique cardinality.",
)

with panel(
    title="Master Table Schema Dictionary",
    description="Detailed attribute metadata for all 25+ columns in the master cleaned dataset.",
):
    column_summary = pd.DataFrame(
        {
            "Column": master_df.columns,
            "Data Type": [str(dtype) for dtype in master_df.dtypes],
            "Non-Null Count": [int(master_df[col].notna().sum()) for col in master_df.columns],
            "Missing Count": [int(master_df[col].isna().sum()) for col in master_df.columns],
            "Missing (%)": [master_df[col].isna().mean() * 100 for col in master_df.columns],
            "Unique Values": [int(master_df[col].nunique()) for col in master_df.columns],
        }
    )

    st.dataframe(
        column_summary,
        width="stretch",
        hide_index=True,
        height=340,
        column_config={
            "Column": st.column_config.TextColumn("Attribute Name", width="large"),
            "Data Type": st.column_config.TextColumn("Data Type", width="medium"),
            "Non-Null Count": st.column_config.NumberColumn("Non-Null Values", format="%,d"),
            "Missing Count": st.column_config.NumberColumn("Missing Values", format="%,d"),
            "Missing (%)": st.column_config.NumberColumn("Missing (%)", format="%.2f%%"),
            "Unique Values": st.column_config.NumberColumn("Unique Values", format="%,d"),
        },
    )

# ============================================================================
# INTERACTIVE COLUMN DISTRIBUTION INSPECTOR
# ============================================================================

section_header(
    title="Interactive Column Distribution Inspector",
    description="Select any numeric or categorical column to visualize its underlying distribution.",
)

with panel(
    title="Feature Distribution Visualizer",
    description="Dynamically profiles selected columns with automated frequency histograms and bar charts.",
):
    col_sel, col_sp = st.columns([1, 2], gap="medium")
    with col_sel:
        inspect_col = st.selectbox(
            "Select Column to Profile",
            options=list(master_df.columns),
            index=list(master_df.columns).index("price") if "price" in master_df.columns else 0,
        )

    col_series = master_df[inspect_col].dropna()

    if pd.api.types.is_numeric_dtype(col_series):
        dist_fig = px.histogram(
            master_df,
            x=inspect_col,
            nbins=35,
            title=f"Numerical Distribution: {inspect_col}",
            color_discrete_sequence=[PRIMARY_COLOR],
        )
        dist_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
            margin=dict(l=30, r=20, t=35, b=30),
            height=320,
        )
        st.plotly_chart(dist_fig, width="stretch")
    else:
        top_cats = col_series.value_counts().head(12).reset_index()
        top_cats.columns = [inspect_col, "Count"]
        cat_fig = px.bar(
            top_cats,
            x=inspect_col,
            y="Count",
            title=f"Top Categories / Frequencies: {inspect_col}",
            color_discrete_sequence=CHART_PALETTE,
        )
        cat_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
            margin=dict(l=30, r=20, t=35, b=30),
            height=320,
        )
        st.plotly_chart(cat_fig, width="stretch")

# ============================================================================
# SEARCHABLE DATA PREVIEW & EXPORTS
# ============================================================================

section_header(
    title="Searchable Data Preview & Export",
    description="Filter, search, and export slices of the master dataset.",
)

with panel(
    title="Data Preview Grid",
    description="Exportable records table with dynamic column selection and full-text keyword search.",
):
    col_ctrl1, col_ctrl2 = st.columns([2, 1], gap="medium")

    with col_ctrl1:
        selected_columns = st.multiselect(
            "Columns to Display",
            options=list(master_df.columns),
            default=list(master_df.columns[: min(8, len(master_df.columns))]),
        )

    with col_ctrl2:
        preview_rows = st.selectbox(
            "Rows to Display",
            options=[25, 50, 100, 250, 500],
            index=1,
        )

    search_text = st.text_input(
        "Search Dataset Records",
        placeholder="Enter search keyword across selected columns...",
    )

    if not selected_columns:
        st.info("Select at least one column to display the data preview.")
    else:
        preview_df = master_df[selected_columns].copy()

        if search_text.strip():
            search_val = search_text.strip().lower()
            mask = (
                preview_df.astype(str)
                .apply(lambda col: col.str.lower().str.contains(search_val, na=False))
                .any(axis=1)
            )
            preview_df = preview_df[mask]

        preview_slice = preview_df.head(preview_rows)

        st.dataframe(
            preview_slice,
            width="stretch",
            hide_index=True,
            height=380,
        )

        col_exp1, col_exp2, col_sp = st.columns([1, 1, 2], gap="small")
        with col_exp1:
            csv_download(preview_slice, filename="master_data_slice.csv", key="csv_data_exp")
        with col_exp2:
            excel_download(preview_slice, filename="master_data_slice.xlsx", key="excel_data_exp")