"""
Multi-Grain Revenue Forecast Dashboard.
========================================
Enterprise Predictive Analytics Engine

Responsibilities:
1. Load prepared multi-grain revenue forecast data.
2. Provide dynamic dimension selection (Total Marketplace, Product Categories, Regional Markets).
3. Parameterize executive forecast KPIs for the selected grain.
4. Visualize actual vs. predicted revenue with 90% confidence bands.
5. Display future forecast growth trajectories and confidence widths.
6. Provide an exportable, formatted forecast detail table.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboards.components.alerts import insight_card
from dashboards.components.charts import bar_chart, forecast_chart
from dashboards.components.containers import panel
from dashboards.components.exports import csv_download, excel_download
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.loading_states import loading_spinner
from dashboards.components.section_headers import page_header, section_header
from dashboards.components.tables import render_styled_table
from dashboards.data.loader import get_available_forecast_segments, load_revenue_forecast
from dashboards.data.transformations import prepare_revenue_forecast
from dashboards.utils.html import render_html

# ============================================================================
# CONSTANTS
# ============================================================================

CURRENCY_SYMBOL = "R$"

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Revenue Forecast",
    description=(
        "Project future revenue and evaluate growth trajectories across multiple "
        "business dimensions — including total marketplace revenue, top product categories, "
        "and major regional markets — powered by Prophet time-series models with 90% confidence intervals."
    ),
    status="PROPHET FORECASTING",
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
                color: #F4A261;
                font-size: 8.5px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            ">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#F4A261;"></span>
                PROPHET TIME-SERIES ENGINE
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Multi-Grain Revenue Projections & Financial Planning
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F1FAEE;">
                Evaluate forward 6-month gross merchandise value projections across aggregate marketplace,
                top 5 merchandise categories, and major Brazilian state territories with 90% confidence uncertainty bands.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# MULTI-GRAIN SELECTION CONTROLS
# ============================================================================

section_header(
    title="Forecast Dimension & Grain Selection",
    description=(
        "Select the analytical cut to inspect: total aggregate marketplace revenue, "
        "individual top-performing product categories, or key geographic state markets."
    ),
)

available_segments = get_available_forecast_segments()

with panel(
    title="Forecast Grain & Slicing Toolbar",
    description="Select analytical dimension cut to project future revenue across total, category, or regional horizons.",
    badge="GRAIN SELECTOR",
):
    col_dim, col_val = st.columns([1, 1], gap="medium")

    with col_dim:
        dimension_choice = st.selectbox(
            "Forecast Dimension",
            options=["Total Marketplace Revenue", "By Product Category", "By Regional State / Market"],
            index=0,
            help="Switch between aggregate marketplace projections and specific category or regional cuts.",
        )

    selected_segment_type = "total"
    selected_segment_value = "All"
    segment_display_label = "Total Marketplace"

    if dimension_choice == "Total Marketplace Revenue":
        selected_segment_type = "total"
        selected_segment_value = "All"
        segment_display_label = "Total Marketplace"
        with col_val:
            st.text_input("Segment Filter", value="All Marketplace Orders", disabled=True)

    elif dimension_choice == "By Product Category":
        selected_segment_type = "category"
        categories_list = available_segments.get("category", ["bed_bath_table"])
        with col_val:
            selected_segment_value = st.selectbox(
                "Select Product Category",
                options=categories_list,
                index=0,
                format_func=lambda x: x.replace("_", " ").title(),
                help="Top 5 highest-revenue marketplace categories evaluated independently.",
            )
        segment_display_label = f"Category: {selected_segment_value.replace('_', ' ').title()}"

    elif dimension_choice == "By Regional State / Market":
        selected_segment_type = "region"
        regions_list = available_segments.get("region", ["SP"])
        with col_val:
            selected_segment_value = st.selectbox(
                "Select State / Region",
                options=regions_list,
                index=0,
                help="Top 5 customer volume states in Brazil evaluated independently.",
            )
        segment_display_label = f"Region: {selected_segment_value}"

# ============================================================================
# LOAD & FILTER FORECAST DATA
# ============================================================================

with loading_spinner(f"Loading forecast for {segment_display_label}..."):
    try:
        raw_forecast_data = load_revenue_forecast(
            segment_type=selected_segment_type,
            segment_value=selected_segment_value,
        )
    except FileNotFoundError as exc:
        st.error("Revenue forecast data could not be found.")
        st.caption(str(exc))
        st.stop()
    except Exception as exc:
        st.error("An unexpected error occurred while loading revenue forecast data.")
        st.caption(str(exc))
        st.stop()

if raw_forecast_data is None or raw_forecast_data.empty:
    st.warning(f"No forecast data available for {segment_display_label}.")
    st.stop()

try:
    forecast_df = prepare_revenue_forecast(raw_forecast_data)
except Exception as exc:
    st.error("Revenue forecast data could not be prepared.")
    st.caption(str(exc))
    st.stop()

historical_df = forecast_df[forecast_df["actual_revenue"].notna()].copy()
future_forecast_df = forecast_df[
    forecast_df["actual_revenue"].isna() & forecast_df["predicted_revenue"].notna()
].copy()

if future_forecast_df.empty and not historical_df.empty:
    last_actual_month = historical_df["month"].max()
    future_forecast_df = forecast_df[
        (forecast_df["month"] > last_actual_month) & forecast_df["predicted_revenue"].notna()
    ].copy()

# ============================================================================
# METRICS COMPUTATION
# ============================================================================

if not historical_df.empty:
    total_actual_revenue = historical_df["actual_revenue"].dropna().sum()
    latest_actual_revenue = historical_df.sort_values("month")["actual_revenue"].iloc[-1]
else:
    total_actual_revenue = 0.0
    latest_actual_revenue = 0.0

if not future_forecast_df.empty:
    total_future_forecast = future_forecast_df["predicted_revenue"].dropna().sum()
    final_forecast_revenue = future_forecast_df.sort_values("month")["predicted_revenue"].iloc[-1]
    forecast_start = future_forecast_df["month"].min()
    forecast_end = future_forecast_df["month"].max()
    forecast_periods = len(future_forecast_df)
else:
    total_future_forecast = 0.0
    final_forecast_revenue = 0.0
    forecast_start = None
    forecast_end = None
    forecast_periods = 0

forecast_growth = None
if latest_actual_revenue > 0 and not future_forecast_df.empty:
    first_forecast_revenue = future_forecast_df.sort_values("month")["predicted_revenue"].iloc[0]
    if pd.notna(first_forecast_revenue):
        forecast_growth = ((first_forecast_revenue - latest_actual_revenue) / latest_actual_revenue) * 100

if not future_forecast_df.empty:
    future_forecast_df["forecast_range"] = (
        future_forecast_df["upper_bound"] - future_forecast_df["lower_bound"]
    )
    average_forecast_range = future_forecast_df["forecast_range"].dropna().mean()
else:
    average_forecast_range = None

# ============================================================================
# FORECAST OVERVIEW KPIs
# ============================================================================

section_header(
    title=f"Forecast Overview ({segment_display_label})",
    description="Key financial metrics summarizing historical baseline and projected 6-month horizon.",
)

kpi_cols = st.columns(4, gap="large")

with kpi_cols[0]:
    kpi_card(
        label="Observed Historical Revenue",
        value=f"{CURRENCY_SYMBOL} {total_actual_revenue:,.0f}",
        delta="Historical delivered GMV",
        delta_type="neutral",
    )

with kpi_cols[1]:
    kpi_card(
        label="6-Month Projected GMV",
        value=f"{CURRENCY_SYMBOL} {total_future_forecast:,.0f}",
        delta=f"Terminal: {CURRENCY_SYMBOL} {final_forecast_revenue:,.0f}",
        delta_type="positive",
    )

with kpi_cols[2]:
    delta_str = f"{forecast_growth:+.1f}% vs last month" if forecast_growth is not None else "Baseline trajectory"
    kpi_card(
        label="Horizon Trajectory",
        value=f"{forecast_growth:+.1f}%" if forecast_growth is not None else "Steady",
        delta=delta_str,
        delta_type="positive" if (forecast_growth and forecast_growth > 0) else "neutral",
    )

with kpi_cols[3]:
    kpi_card(
        label="Forecast Duration",
        value=f"{forecast_periods} Months",
        delta=f"{forecast_start.strftime('%b %Y') if forecast_start else ''} – {forecast_end.strftime('%b %Y') if forecast_end else ''}",
        delta_type="neutral",
    )

# ============================================================================
# ACTUAL VS FORECAST TREND
# ============================================================================

section_header(
    title="Revenue Forecast Trend & Uncertainty Band",
    description="Historical actuals alongside Prophet model fitted trend and 90% confidence interval shading.",
)

with panel(
    title=f"Revenue Trajectory: {segment_display_label}",
    description="Monthly revenue trajectory with lower/upper confidence bounds (BRL).",
    badge="PROPHET HORIZON",
    footer_insight="Point estimates project stable forward momentum with 90% confidence bands.",
):
    forecast_chart(
        dataframe=forecast_df,
        date_column="month",
        actual_column="actual_revenue",
        forecast_column="predicted_revenue",
        lower_column="lower_bound",
        upper_column="upper_bound",
        title=None,
        x_title="Month",
        y_title="Revenue (R$)",
        height=440,
    )

# ============================================================================
# MONTHLY FORECAST BREAKDOWN & CONFIDENCE
# ============================================================================

col_chart, col_conf = st.columns([1.35, 1], gap="large")

with col_chart:
    with panel(
        title="Projected Monthly Revenue",
        description="Month-by-month revenue projections across the future window.",
        badge="PROJECTION CADENCE",
        footer_insight="Aggregate projections maintain consistent run rates across the 6-month forecast window.",
    ):
        if not future_forecast_df.empty:
            forecast_chart_df = future_forecast_df[["month", "predicted_revenue"]].copy()
            forecast_chart_df["period"] = forecast_chart_df["month"].dt.strftime("%b %Y")

            bar_chart(
                dataframe=forecast_chart_df,
                x="period",
                y="predicted_revenue",
                title=None,
                x_title="Forecast Period",
                y_title="Predicted Revenue (R$)",
                height=360,
                text=False,
            )

with col_conf:
    with panel(
        title="Confidence & Planning Risk",
        description="Assessing model uncertainty interval widths for risk management.",
        badge="RISK BOUNDS",
        footer_insight="Model risk corridor is bounded between conservative and optimistic operational cases.",
    ):
        range_val = f"{CURRENCY_SYMBOL} {average_forecast_range:,.0f}" if average_forecast_range is not None else "N/A"
        kpi_card(
            label="Average 90% Spread Width",
            value=range_val,
            delta="Upper – Lower 90% spread",
            delta_type="neutral",
        )

        render_html("<div style='height: 12px;'></div>")

        if not future_forecast_df.empty:
            lower_sum = float(future_forecast_df["lower_bound"].sum())
            upper_sum = float(future_forecast_df["upper_bound"].sum())
            point_sum = float(total_future_forecast)
            bear_diff_pct = ((lower_sum - point_sum) / point_sum * 100) if point_sum > 0 else 0.0
            bull_diff_pct = ((upper_sum - point_sum) / point_sum * 100) if point_sum > 0 else 0.0

            render_html(f"""
            <div class="scenario-planning-card">
                <div class="scenario-planning-header">
                    <div class="scenario-planning-title">
                        <span class="scenario-header-icon">📊</span>
                        <span>Financial Planning Guidance</span>
                    </div>
                    <span class="scenario-segment-pill">{segment_display_label}</span>
                </div>
                <div class="scenario-grid">
                    <div class="scenario-item scenario-bear">
                        <div class="scenario-label">BEAR CASE (90% LOWER)</div>
                        <div class="scenario-value">R$ {lower_sum:,.0f}</div>
                        <div class="scenario-badge bear-badge">{bear_diff_pct:.1f}% vs Base</div>
                    </div>
                    <div class="scenario-item scenario-base">
                        <div class="scenario-label">POINT ESTIMATE (BASE)</div>
                        <div class="scenario-value">R$ {point_sum:,.0f}</div>
                        <div class="scenario-badge base-badge">Core Budget Target</div>
                    </div>
                    <div class="scenario-item scenario-bull">
                        <div class="scenario-label">BULL CASE (90% UPPER)</div>
                        <div class="scenario-value">R$ {upper_sum:,.0f}</div>
                        <div class="scenario-badge bull-badge">+{bull_diff_pct:.1f}% vs Base</div>
                    </div>
                </div>
            </div>
            """)

# ============================================================================
# FORECAST DETAIL TABLE & EXPORTS
# ============================================================================

section_header(
    title="Detailed Monthly Forecast Data",
    description="Numerical breakdown of point predictions and confidence interval boundaries.",
)

with panel(
    title="Forecast Drilldown Table",
    description="Exportable monthly breakdown with 90% lower and upper bounds formatted in Brazilian Real (R$).",
):
    if not future_forecast_df.empty:
        detail_df = future_forecast_df[
            ["month", "predicted_revenue", "lower_bound", "upper_bound"]
        ].copy()

        detail_df["Month"] = detail_df["month"].dt.strftime("%B %Y")
        detail_df["Forecast Revenue (R$)"] = detail_df["predicted_revenue"]
        detail_df["Lower Bound 90% (R$)"] = detail_df["lower_bound"]
        detail_df["Upper Bound 90% (R$)"] = detail_df["upper_bound"]

        display_table = detail_df[
            ["Month", "Forecast Revenue (R$)", "Lower Bound 90% (R$)", "Upper Bound 90% (R$)"]
        ]

        render_styled_table(
            display_table,
            column_formats={
                "Forecast Revenue (R$)": "R$ {:,.2f}",
                "Lower Bound 90% (R$)": "R$ {:,.2f}",
                "Upper Bound 90% (R$)": "R$ {:,.2f}",
            },
        )

        col_exp1, col_exp2, col_sp = st.columns([1, 1, 2], gap="small")
        with col_exp1:
            csv_download(display_table, filename=f"revenue_forecast_{selected_segment_type}_{selected_segment_value}.csv", key="csv_rev_fc")
        with col_exp2:
            excel_download(display_table, filename=f"revenue_forecast_{selected_segment_type}_{selected_segment_value}.xlsx", key="excel_rev_fc")