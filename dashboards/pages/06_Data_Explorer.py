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
from dashboards.components.tables import render_styled_table
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
                DATA GOVERNANCE & SCHEMA PROFILER
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Master Dataset Catalog & Quality Inspection Workspace
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F1FAEE;">
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
    badge="DATA DICTIONARY",
    footer_insight="All transaction attributes are strictly typed and indexed for high performance.",
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

    render_styled_table(
        column_summary,
        column_formats={
            "Non-Null Count": "{:,.0f}",
            "Missing Count": "{:,.0f}",
            "Missing (%)": "{:.2f}%",
            "Unique Values": "{:,.0f}",
        },
        max_height=340,
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
    badge="PROFILER",
    footer_insight="Dynamically computes cardinality, frequency bins, and distributions.",
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
            color_discrete_sequence=[PRIMARY_COLOR],
        )
        dist_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
            margin=dict(l=30, r=20, t=15, b=30),
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
            color_discrete_sequence=CHART_PALETTE,
        )
        cat_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
            margin=dict(l=30, r=20, t=15, b=30),
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

# ============================================================================
# INTERACTIVE DUCKDB SQL STUDIO (MODERN DATA STACK)
# ============================================================================

section_header(
    title="Interactive DuckDB SQL Studio",
    description="Execute custom SQL queries directly against the in-process OLAP analytics engine.",
)

with panel(
    title="SQL Query Console & View Explorer",
    description="Query registered analytical views: v_master_transactions, v_orders_deduplicated, v_customer_rfm, v_delivery_performance, v_monthly_kpis_mom.",
):
    import time
    from pathlib import Path
    try:
        import duckdb
        has_duckdb = True
    except ImportError:
        duckdb = None
        has_duckdb = False

    db_path = Path(__file__).resolve().parents[2] / "data" / "analytics_engine.duckdb"

    preset_queries = {
        "1. Monthly GMV & MoM Growth (v_monthly_kpis_mom)": """SELECT 
    month,
    monthly_revenue,
    total_orders,
    average_order_value,
    prev_month_revenue,
    mom_growth_pct
FROM v_monthly_kpis_mom 
ORDER BY month DESC 
LIMIT 12;""",

        "2. Customer RFM Distribution (v_customer_rfm)": """SELECT 
    CASE 
        WHEN frequency > 1 THEN 'Repeat Buyer'
        WHEN recency <= 180 THEN 'Recent Buyer'
        ELSE 'Lapsed Buyer'
    END AS customer_type,
    COUNT(*) AS total_customers,
    ROUND(AVG(recency), 1) AS avg_recency_days,
    ROUND(AVG(monetary), 2) AS avg_monetary_spend,
    ROUND(SUM(monetary), 2) AS total_segment_revenue
FROM v_customer_rfm
GROUP BY 1
ORDER BY total_segment_revenue DESC;""",

        "3. Delivery SLA vs Customer Dissatisfaction (v_delivery_performance)": """SELECT 
    is_delayed,
    COUNT(*) AS total_orders,
    ROUND(AVG(delivery_time_days), 1) AS avg_delivery_days,
    ROUND(AVG(low_review) * 100, 2) AS low_review_rate_pct,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM v_delivery_performance
GROUP BY is_delayed
ORDER BY is_delayed ASC;""",

        "4. Top 10 Product Categories by Revenue (v_master_transactions)": """SELECT 
    product_category_name_english AS category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(price), 2) AS gross_sales_value,
    ROUND(AVG(price), 2) AS avg_item_price,
    ROUND(AVG(review_score), 2) AS avg_rating
FROM v_master_transactions
GROUP BY product_category_name_english
ORDER BY gross_sales_value DESC
LIMIT 10;""",

        "5. Order-Level Deduplicated Payments (v_orders_deduplicated)": """SELECT 
    order_id,
    customer_state,
    product_category_name_english,
    total_order_value,
    payment_installments,
    review_score,
    purchase_timestamp
FROM v_orders_deduplicated
ORDER BY total_order_value DESC
LIMIT 15;"""
    }

    preset_name = st.selectbox(
        "Select Preset SQL Query Template",
        options=list(preset_queries.keys()),
        index=0,
    )

    sql_query = st.text_area(
        "SQL Query (DuckDB / SQL Dialect)",
        value=preset_queries[preset_name],
        height=180,
        help="Write any valid SQL query. You can query any registered view or table.",
    )

    col_btn, col_info = st.columns([1, 4])
    with col_btn:
        run_query = st.button("▶ Run SQL Query", type="primary", use_container_width=True)

    if run_query or "sql_result_df" in st.session_state:
        if run_query:
            try:
                t_start = time.time()
                if has_duckdb and duckdb is not None:
                    if db_path.exists():
                        con = duckdb.connect(str(db_path), read_only=True)
                    else:
                        con = duckdb.connect()
                        con.register("v_master_transactions", master_df)
                    
                    result_df = con.execute(sql_query).fetchdf()
                    con.close()
                else:
                    import sqlite3
                    con = sqlite3.connect(":memory:")
                    master_df.to_sql("v_master_transactions", con, index=False, if_exists="replace")
                    result_df = pd.read_sql_query(sql_query, con)
                    con.close()

                query_time_ms = (time.time() - t_start) * 1000
                st.session_state["sql_result_df"] = result_df
                st.session_state["sql_query_time"] = query_time_ms
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
                st.session_state.pop("sql_result_df", None)

        if "sql_result_df" in st.session_state and st.session_state["sql_result_df"] is not None:
            res_df = st.session_state["sql_result_df"]
            q_time = st.session_state.get("sql_query_time", 0.0)

            st.success(f"✓ Query executed in **{q_time:.1f} ms** — Returned **{len(res_df):,}** rows and **{len(res_df.columns)}** columns.")
            st.dataframe(res_df, width="stretch", height=300)
            
            csv_download(res_df, filename="duckdb_query_result.csv", key="sql_export_csv")