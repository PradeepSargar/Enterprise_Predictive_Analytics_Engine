"""
Executive Overview
==================
Enterprise Predictive Analytics Engine

Strategic executive cockpit providing a high-level, decision-oriented view of:
- Marketplace Financial Performance (GMV, Orders, AOV)
- Customer Base & Retention Dynamics (RFM Segmentation, Repeat Rate)
- Predictive Revenue Outlook (Prophet Multi-Grain Horizon & Confidence Bands)
- Strategic Business Insights & Growth Levers
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

# ============================================================================
# REUSABLE COMPONENTS & UTILITIES
# ============================================================================

from dashboards.components.alerts import insight_card
from dashboards.components.charts import (
    bar_chart,
    donut_chart,
    forecast_chart,
    horizontal_bar_chart,
    line_chart,
)
from dashboards.components.containers import panel, two_column_layout
from dashboards.components.exports import export_buttons
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.loading_states import loading_spinner
from dashboards.components.section_headers import page_header, section_header
from dashboards.components.status_indicators import live_status
from dashboards.utils.constants import (
    CURRENCY_SYMBOL,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR,
    DANGER_COLOR,
)
from dashboards.utils.formatting import format_currency, format_number, format_percent
from dashboards.utils.html import render_html
from dashboards.state.filters import init_filter_state, get_filter, set_filter

# ============================================================================
# DATA & TRANSFORMATION LAYER
# ============================================================================

from dashboards.data.loader import (
    get_available_forecast_segments,
    load_customer_segments,
    load_master_data,
    load_revenue_forecast,
)
from dashboards.data.transformations import (
    calculate_customer_segment_summary,
    calculate_executive_kpis,
    calculate_monthly_business_performance,
    prepare_revenue_forecast,
)


# ============================================================================
# STATE INITIALIZATION & DATA LOADING
# ============================================================================

init_filter_state()

with loading_spinner("Loading executive analytics and predictive data..."):
    master_df = load_master_data()
    customer_segments_df = load_customer_segments()
    revenue_forecast_df = load_revenue_forecast()

# ============================================================================
# PAGE HEADER & STATUS
# ============================================================================

page_header(
    title="Executive Overview",
    description=(
        "Strategic cockpit tracking marketplace revenue, customer health, "
        "and 6-month predictive trajectory across the Olist ecosystem."
    ),
)

live_status("ENTERPRISE ANALYTICS • REAL-TIME INTELLIGENCE")


# ============================================================================
# EXECUTIVE HERO BANNER & PLATFORM HIGHLIGHTS
# ============================================================================

total_gmv_val = master_df.drop_duplicates(subset=["order_id"])["payment_value"].sum()
total_orders_val = master_df["order_id"].nunique()
total_cust_val = master_df["customer_unique_id"].nunique()

render_html(
    f"""
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0B1220 0%, #172554 60%, #1E3A8A 100%);
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.08);
    ">
        <div style="
            position: absolute;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0) 70%);
            top: -60px;
            right: 40px;
            pointer-events: none;
        "></div>

        <div style="position: relative; z-index: 2;">
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 0.25rem 0.65rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.18);
                color: #93C5FD;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.75rem;
            ">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#38BDF8;"></span>
                Marketplace Performance Summary
            </div>

            <div style="
                color: #FFFFFF;
                font-size: 22px;
                font-weight: 800;
                line-height: 1.3;
                margin-bottom: 0.5rem;
            ">
                Driving <span style="color: #60A5FA;">R$15.4M+</span> in Gross Marketplace Volume across <span style="color: #93C5FD;">96.5k Orders</span>
            </div>

            <div style="
                color: #94A3B8;
                font-size: 13px;
                line-height: 1.5;
                max-width: 860px;
            ">
                Comprehensive e-commerce intelligence platform integrating descriptive transaction analytics, 
                customer RFM segmentation, delivery dissatisfaction risk modeling, and Prophet multi-grain revenue forecasting.
            </div>
        </div>
    </div>
    """
)


# ============================================================================
# EXECUTIVE CONTROLS & FILTER RIBBON
# ============================================================================

with st.expander("🔍 Filter & Slice Executive Data", expanded=False):
    col_f1, col_f2, col_f3 = st.columns(3)

    available_categories = sorted(
        [cat for cat in master_df["product_category_name_english"].dropna().unique()]
    )
    available_states = sorted(
        [stt for stt in master_df["customer_state"].dropna().unique()]
    )

    with col_f1:
        selected_states = st.multiselect(
            "Customer Regional Market (State)",
            options=available_states,
            default=[],
            help="Filter executive KPIs and trends by customer location (e.g., SP, RJ, MG).",
            placeholder="All 27 Brazilian States",
        )

    with col_f2:
        selected_categories = st.multiselect(
            "Product Category",
            options=available_categories,
            default=[],
            help="Filter executive analytics by product category.",
            placeholder="All Product Categories",
        )

    with col_f3:
        min_rating = st.slider(
            "Minimum Review Rating",
            min_value=1,
            max_value=5,
            value=1,
            step=1,
            help="Filter transactions by customer feedback score.",
        )

# Apply active filters to master_df for dynamic slicing
filtered_df = master_df.copy()
if selected_states:
    filtered_df = filtered_df[filtered_df["customer_state"].isin(selected_states)]
if selected_categories:
    filtered_df = filtered_df[
        filtered_df["product_category_name_english"].isin(selected_categories)
    ]
if min_rating > 1:
    filtered_df = filtered_df[filtered_df["review_score"] >= min_rating]

# Fallback if filters return empty
if filtered_df.empty:
    st.warning("⚠️ No records match the active filter criteria. Showing all marketplace data.")
    filtered_df = master_df.copy()


# ============================================================================
# EXECUTIVE KPI CALCULATION & GRID
# ============================================================================

executive_kpis = calculate_executive_kpis(filtered_df)
monthly_business = calculate_monthly_business_performance(filtered_df)
customer_segment_summary = calculate_customer_segment_summary(customer_segments_df)

section_header(
    title="Executive KPI Scorecard",
    description=(
        "Core health and operational metrics computed across unique orders and customers."
    ),
)

kpi_cols = st.columns(6, gap="small")

with kpi_cols[0]:
    kpi_card(
        label="Total Revenue",
        value=f"R${executive_kpis['total_revenue']:,.0f}",
        delta="Order-level GMV",
        delta_type="positive",
        accent="blue",
        icon="💰",
    )

with kpi_cols[1]:
    kpi_card(
        label="Total Orders",
        value=f"{executive_kpis['total_orders']:,}",
        delta="Unique transactions",
        delta_type="neutral",
        accent="purple",
        icon="📦",
    )

with kpi_cols[2]:
    kpi_card(
        label="Unique Buyers",
        value=f"{executive_kpis['total_customers']:,}",
        delta="Distinct consumers",
        delta_type="neutral",
        accent="green",
        icon="👥",
    )

with kpi_cols[3]:
    kpi_card(
        label="Average Order Value",
        value=f"R${executive_kpis['average_order_value']:,.0f}",
        delta="Revenue per basket",
        delta_type="neutral",
        accent="amber",
        icon="🏷️",
    )

with kpi_cols[4]:
    repeat_rate = executive_kpis["repeat_customer_rate"]
    kpi_card(
        label="Repeat Buyer Rate",
        value=f"{repeat_rate:.1%}",
        delta="Critical retention lever" if repeat_rate < 0.10 else "Healthy retention",
        delta_type="negative" if repeat_rate < 0.10 else "positive",
        accent="red" if repeat_rate < 0.10 else "green",
        icon="🔄",
    )

with kpi_cols[5]:
    review_score = executive_kpis["average_review_score"]
    low_review_rate = executive_kpis["low_review_rate"]
    kpi_card(
        label="Average CSAT",
        value=f"{review_score:.2f} / 5",
        delta=f"{low_review_rate:.1%} low reviews (1-2★)",
        delta_type="positive" if review_score >= 4.0 else "negative",
        accent="green" if review_score >= 4.0 else "amber",
        icon="⭐",
    )


# ============================================================================
# FINANCIAL PERFORMANCE & COMMERCIAL VOLUME (TABBED)
# ============================================================================

section_header(
    title="Marketplace Financial & Volume Velocity",
    description=(
        "Historical trajectory, order velocity, and category concentration over time."
    ),
)

tab_revenue, tab_volume, tab_category = st.tabs(
    [
        "📈 Monthly Revenue Trajectory",
        "📦 Order Volume & Basket Size",
        "🏷️ Top Product Categories",
    ]
)

with tab_revenue:
    with panel(
        title="Monthly Revenue Trend (BRL)",
        description="Historical marketplace revenue progression across historical operating months.",
    ):
        if not monthly_business.empty:
            line_chart(
                dataframe=monthly_business,
                x="month",
                y="revenue",
                title=None,
                x_title="Operating Month",
                y_title="Gross Revenue (R$)",
                height=360,
                markers=True,
            )
        else:
            st.info("No monthly business data available for active filters.")

with tab_volume:
    col_v1, col_v2 = two_column_layout(ratio=(1.2, 1.0))
    with col_v1:
        with panel(
            title="Monthly Unique Order Volume",
            description="Number of fulfilled transactions per month.",
        ):
            line_chart(
                dataframe=monthly_business,
                x="month",
                y="orders",
                title=None,
                x_title="Operating Month",
                y_title="Total Orders",
                height=340,
                markers=True,
            )
    with col_v2:
        with panel(
            title="Average Order Value (AOV)",
            description="Average monetary spend per transaction.",
        ):
            line_chart(
                dataframe=monthly_business,
                x="month",
                y="average_order_value",
                title=None,
                x_title="Operating Month",
                y_title="AOV (R$)",
                height=340,
                markers=True,
            )

with tab_category:
    with panel(
        title="Top 10 Categories by Revenue",
        description="Major product categories driving gross marketplace revenue.",
    ):
        top_cats = (
            filtered_df.groupby("product_category_name_english")["payment_value"]
            .sum()
            .reset_index()
            .sort_values("payment_value", ascending=True)
            .tail(10)
        )
        if not top_cats.empty:
            horizontal_bar_chart(
                dataframe=top_cats,
                category="product_category_name_english",
                value="payment_value",
                title=None,
                category_title="Category",
                value_title="Gross Revenue (R$)",
                height=380,
                text=False,
            )
        else:
            st.info("No category data available.")


# ============================================================================
# PREDICTIVE INTELLIGENCE & 6-MONTH REVENUE OUTLOOK
# ============================================================================

section_header(
    title="Predictive Revenue Horizon (6-Month Forecast)",
    description=(
        "Forward-looking revenue projections powered by the Prophet time-series model with 90% confidence intervals."
    ),
)

fc_dimension_col, fc_view_col = st.columns([1, 2])

with fc_dimension_col:
    segments_map = get_available_forecast_segments()
    forecast_cut = st.selectbox(
        "Forecast Dimension Cut",
        options=["Total Marketplace", "By Top Category", "By Top State"],
        index=0,
        help="Switch between total marketplace and granular category or regional state forecasts.",
    )

    if forecast_cut == "By Top Category":
        selected_seg_val = st.selectbox(
            "Select Product Category",
            options=segments_map["category"],
            index=0,
        )
        current_fc_raw = load_revenue_forecast(
            segment_type="category", segment_value=selected_seg_val
        )
    elif forecast_cut == "By Top State":
        selected_seg_val = st.selectbox(
            "Select State / Region",
            options=segments_map["region"],
            index=0,
        )
        current_fc_raw = load_revenue_forecast(
            segment_type="region", segment_value=selected_seg_val
        )
    else:
        selected_seg_val = "All"
        current_fc_raw = load_revenue_forecast(
            segment_type="total", segment_value="All"
        )

    prepared_fc = prepare_revenue_forecast(current_fc_raw)

    # Forecast summary metrics
    future_points = prepared_fc[prepared_fc["actual_revenue"].isna()]
    if not future_points.empty:
        next_month_pred = future_points.iloc[0]["predicted_revenue"]
        terminal_month_pred = future_points.iloc[-1]["predicted_revenue"]
        growth_pct = (terminal_month_pred - next_month_pred) / max(next_month_pred, 1)

        render_html(
            f"""
            <div class="chart-card" style="padding: 1.1rem; margin-top: 0.8rem; background: #F8FAFC; border: 1px solid #E2E8F0;">
                <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 0.4rem;">
                    Forecast Summary ({selected_seg_val})
                </div>
                <div style="font-size: 18px; font-weight: 800; color: #0F172A; margin-bottom: 0.25rem;">
                    {format_currency(terminal_month_pred)} <span style="font-size: 12px; color: #059669; font-weight: 700;">(+{growth_pct:.1%})</span>
                </div>
                <div style="font-size: 11px; color: #475569; line-height: 1.4;">
                    Projected 6-month exit velocity from {format_currency(next_month_pred)}.
                </div>
            </div>
            """
        )

with fc_view_col:
    with panel(
        title=f"Revenue Trajectory & Uncertainty Interval ({forecast_cut})",
        description="Historical actuals (solid line) alongside point forecast (dashed line) and 90% confidence corridor.",
    ):
        forecast_chart(
            dataframe=prepared_fc,
            date_column="month",
            actual_column="actual_revenue",
            forecast_column="predicted_revenue",
            lower_column="lower_bound",
            upper_column="upper_bound",
            x_title="Month",
            y_title="Revenue (R$)",
            height=380,
        )


# ============================================================================
# CUSTOMER INTELLIGENCE & SEGMENT ECONOMICS
# ============================================================================

section_header(
    title="Customer Base Segmentation & RFM Distribution",
    description=(
        "Customer composition across KMeans-identified behavioral clusters (Recency, Frequency, Monetary)."
    ),
)

cust_donut_col, cust_bar_col = two_column_layout(ratio=(1.0, 1.1))

with cust_donut_col:
    with panel(
        title="Customer Cluster Share",
        description="Proportion of total customer base assigned to each RFM segment.",
    ):
        donut_chart(
            dataframe=customer_segment_summary,
            names="segment",
            values="customers",
            height=340,
            hole=0.6,
        )

with cust_bar_col:
    with panel(
        title="Customer Segment Volume",
        description="Absolute count of customers per behavioral segment.",
    ):
        seg_ranking = (
            customer_segment_summary[["segment", "customers"]]
            .copy()
            .sort_values("customers", ascending=True)
        )
        bar_chart(
            dataframe=seg_ranking,
            x="customers",
            y="segment",
            title=None,
            x_title="Customer Count",
            y_title="Segment",
            height=340,
            text=True,
        )

# Segment Detail Table
display_segments = customer_segment_summary.copy()
if not display_segments.empty:
    display_segments["percentage"] = (
        display_segments["percentage"].mul(100).round(1)
    )
    display_segments = display_segments.rename(
        columns={
            "segment": "Customer Segment",
            "customers": "Customer Count",
            "percentage": "Share (%)",
        }
    )

    st.dataframe(
        display_segments,
        width="stretch",
        hide_index=True,
        height=200,
        column_config={
            "Customer Segment": st.column_config.TextColumn("Customer Segment", width="large"),
            "Customer Count": st.column_config.NumberColumn("Customer Count", format="%,d"),
            "Share (%)": st.column_config.NumberColumn("Share (%)", format="%.1f%%"),
        },
    )


# ============================================================================
# STRATEGIC EXECUTIVE INSIGHTS
# ============================================================================

section_header(
    title="Strategic Business Observations & Recommended Actions",
    description=(
        "Actionable takeaways derived from exploratory findings, dissatisfaction classification, and forecasting."
    ),
)

insight_cols = st.columns(3, gap="medium")

with insight_cols[0]:
    insight_card(
        label="RETENTION LEVER",
        title="Overcome 3% Repeat Buyer Bottleneck",
        description=(
            "97% of buyers currently purchase only once. Implementing post-delivery automated "
            "re-engagement, loyalty incentives, and cross-category recommendations can double repeat LTV."
        ),
        insight_type="danger" if repeat_rate < 0.05 else "warning",
    )

with insight_cols[1]:
    insight_card(
        label="LOGISTICS & CSAT",
        title="Mitigate Delivery Friction (16.3% Risk)",
        description=(
            "Delivery delays are the dominant driver of 1-star and 2-star reviews. Proactive transit alerts "
            "and carrier SLA enforcement in regions like RJ can dramatically improve customer satisfaction."
        ),
        insight_type="warning" if low_review_rate >= 0.15 else "success",
    )

with insight_cols[2]:
    insight_card(
        label="GROWTH & EXPANSION",
        title="Scale High-Velocity Category Hubs",
        description=(
            "Top categories (Bed Bath Table, Health Beauty, Watches) and SP state represent over 45% of GMV. "
            "Allocate marketing capital and merchant fulfillment to these stable high-growth hubs."
        ),
        insight_type="success",
    )


# ============================================================================
# EXECUTIVE DATA EXPORT
# ============================================================================

section_header(
    title="Executive Data Export",
    description="Download monthly business performance and executive KPIs for offline analysis and reporting.",
)

export_buttons(
    dataframe=monthly_business,
    filename_prefix="executive_monthly_business_summary",
    sheet_name="Executive Summary",
    key_prefix="exec_overview_export",
)