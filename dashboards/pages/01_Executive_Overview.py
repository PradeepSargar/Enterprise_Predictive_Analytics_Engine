"""
Executive Overview page for the Enterprise Predictive Analytics Engine.

This page provides a high-level executive view of:

- Business performance
- Customer base
- Revenue trends
- Revenue forecast
- Customer segmentation
- Executive business insights

All data is loaded through the centralized data layer.

No business calculations are performed directly inside the page.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# REUSABLE COMPONENTS
# ============================================================================

from dashboards.components.alerts import (
    insight_card,
)

from dashboards.components.charts import (
    bar_chart,
    donut_chart,
    forecast_chart,
    line_chart,
)

from dashboards.components.containers import (
    panel,
    two_column_layout,
)

from dashboards.components.exports import (
    export_buttons,
)

from dashboards.components.kpi_cards import (
    kpi_card,
)

from dashboards.components.section_headers import (
    page_header,
    section_header,
)

from dashboards.components.status_indicators import (
    live_status,
)

from dashboards.components.tooltips import (
    metric_help,
)


# ============================================================================
# DATA LAYER
# ============================================================================

from dashboards.data.loader import (
    load_customer_segments,
    load_master_data,
    load_revenue_forecast,
)


# ============================================================================
# TRANSFORMATION LAYER
# ============================================================================

from dashboards.data.transformations import (
    calculate_customer_segment_summary,
    calculate_executive_kpis,
    calculate_monthly_business_performance,
    prepare_revenue_forecast,
)


# ============================================================================
# DATA LOADING
# ============================================================================

master_df = load_master_data()

customer_segments_df = (
    load_customer_segments()
)

revenue_forecast_df = (
    load_revenue_forecast()
)


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

executive_kpis = (
    calculate_executive_kpis(
        master_df
    )
)

monthly_business = (
    calculate_monthly_business_performance(
        master_df
    )
)

customer_segment_summary = (
    calculate_customer_segment_summary(
        customer_segments_df
    )
)

forecast_df = (
    prepare_revenue_forecast(
        revenue_forecast_df
    )
)


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="Executive Overview",
    description=(
        "Enterprise performance, customer intelligence, "
        "and predictive outlook."
    ),
)


live_status(
    "LIVE ANALYTICS"
)


# ============================================================================
# BUSINESS PERFORMANCE
# ============================================================================

section_header(
    title="Business Performance",
    description=(
        "Core business indicators derived from the processed "
        "order and customer datasets."
    ),
)


# ============================================================================
# KPI ROW
# ============================================================================

kpi_columns = st.columns(
    6,
    gap="small",
)


# ----------------------------------------------------------------------------
# Revenue
# ----------------------------------------------------------------------------

with kpi_columns[0]:

    kpi_card(
        label="Total Revenue",
        value=(
            f"₹{executive_kpis['total_revenue']:,.0f}"
        ),
        delta="Actual order-level revenue",
        delta_type="positive",
    )


# ----------------------------------------------------------------------------
# Orders
# ----------------------------------------------------------------------------

with kpi_columns[1]:

    kpi_card(
        label="Total Orders",
        value=(
            f"{executive_kpis['total_orders']:,}"
        ),
        delta="Unique orders",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Customers
# ----------------------------------------------------------------------------

with kpi_columns[2]:

    kpi_card(
        label="Total Customers",
        value=(
            f"{executive_kpis['total_customers']:,}"
        ),
        delta="Unique customers",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Average Order Value
# ----------------------------------------------------------------------------

with kpi_columns[3]:

    kpi_card(
        label="Average Order Value",
        value=(
            f"₹{executive_kpis['average_order_value']:,.0f}"
        ),
        delta="Revenue per order",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Repeat Customer Rate
# ----------------------------------------------------------------------------

with kpi_columns[4]:

    kpi_card(
        label="Repeat Customer Rate",
        value=(
            f"{executive_kpis['repeat_customer_rate']:.1%}"
        ),
        delta="Retention indicator",
        delta_type=(
            "positive"
            if executive_kpis[
                "repeat_customer_rate"
            ] >= 0.20
            else "negative"
        ),
    )


# ----------------------------------------------------------------------------
# Average Review
# ----------------------------------------------------------------------------

with kpi_columns[5]:

    kpi_card(
        label="Average Review",
        value=(
            f"{executive_kpis['average_review_score']:.2f}/5"
        ),
        delta="Customer satisfaction",
        delta_type=(
            "positive"
            if executive_kpis[
                "average_review_score"
            ] >= 4
            else "negative"
        ),
    )


# ============================================================================
# KPI CONTEXT
# ============================================================================

metric_help(
    metric_name="Average Order Value",
    explanation=(
        "Total order-level revenue divided by the number "
        "of unique orders."
    ),
)


# ============================================================================
# BUSINESS PERFORMANCE ANALYTICS
# ============================================================================

section_header(
    title="Business Performance Trends",
    description=(
        "Historical monthly revenue and order activity."
    ),
)


left_column, right_column = two_column_layout(
    ratio=(1.7, 1.0),
)


# ----------------------------------------------------------------------------
# Revenue Trend
# ----------------------------------------------------------------------------

with left_column:

    with panel(
        title="Monthly Revenue",
        description=(
            "Actual revenue generated across the available "
            "historical period."
        ),
    ):

        line_chart(
            dataframe=monthly_business,
            x="month",
            y="revenue",
            x_title="Month",
            y_title="Revenue",
            height=360,
            markers=False,
        )


# ----------------------------------------------------------------------------
# Order Trend
# ----------------------------------------------------------------------------

with right_column:

    with panel(
        title="Monthly Orders",
        description=(
            "Monthly unique order volume."
        ),
    ):

        line_chart(
            dataframe=monthly_business,
            x="month",
            y="orders",
            x_title="Month",
            y_title="Orders",
            height=360,
            markers=False,
        )


# ============================================================================
# PREDICTIVE INTELLIGENCE
# ============================================================================

section_header(
    title="Predictive Intelligence",
    description=(
        "Revenue outlook based on the project's forecasting model."
    ),
)


with panel(
    title="Revenue Forecast",
    description=(
        "Historical actual revenue compared with predicted revenue "
        "and the model confidence interval."
    ),
):

    forecast_chart(
        dataframe=forecast_df,
        date_column="month",
        actual_column="actual_revenue",
        forecast_column="predicted_revenue",
        lower_column="lower_bound",
        upper_column="upper_bound",
        x_title="Month",
        y_title="Revenue",
        height=440,
    )


# ============================================================================
# CUSTOMER INTELLIGENCE
# ============================================================================

section_header(
    title="Customer Intelligence",
    description=(
        "Customer base composition and segment concentration "
        "based on the RFM segmentation results."
    ),
)


customer_column, customer_ranking_column = two_column_layout(
    ratio=(1.0, 1.0),
)


# ----------------------------------------------------------------------------
# Segment Distribution
# ----------------------------------------------------------------------------

with customer_column:

    with panel(
        title="Customer Segment Distribution",
        description=(
            "Share of customers assigned to each analytical segment."
        ),
    ):

        donut_chart(
            dataframe=customer_segment_summary,
            names="segment",
            values="customers",
            height=380,
        )


# ----------------------------------------------------------------------------
# Segment Ranking
# ----------------------------------------------------------------------------

with customer_ranking_column:

    with panel(
        title="Customer Segment Ranking",
        description=(
            "Rank segments by the number of customers they contain."
        ),
    ):

        segment_ranking = (
            customer_segment_summary[
                [
                    "segment",
                    "customers",
                ]
            ]
            .copy()
            .sort_values(
                "customers",
                ascending=True,
            )
        )

        if not segment_ranking.empty:

            bar_chart(
                dataframe=segment_ranking,
                x="customers",
                y="segment",
                title=None,
                x_title="Customers",
                y_title="Segment",
                height=380,
            )

        else:

            st.info(
                "No customer segment data is available."
            )


# ============================================================================
# CUSTOMER SEGMENT DETAIL
# ============================================================================

section_header(
    title="Segment Detail",
    description=(
        "Customer count and percentage contribution for each segment."
    ),
)


display_segments = (
    customer_segment_summary
    .copy()
)


if not display_segments.empty:

    display_segments[
        "percentage"
    ] = (
        display_segments[
            "percentage"
        ]
        .mul(100)
        .round(1)
    )


    display_segments = (
        display_segments.rename(
            columns={
                "segment": "Segment",
                "customers": "Customers",
                "percentage": "Share (%)",
            }
        )
    )


    st.dataframe(
        display_segments,
        use_container_width=True,
        hide_index=True,
        height=220,
        column_config={

            "Segment": st.column_config.TextColumn(
                "Segment",
                width="large",
            ),

            "Customers": st.column_config.NumberColumn(
                "Customers",
                format="%,d",
            ),

            "Share (%)": st.column_config.NumberColumn(
                "Share (%)",
                format="%.1f%%",
            ),
        },
    )

else:

    st.info(
        "No customer segment data is available."
    )


# ============================================================================
# EXECUTIVE INSIGHTS
# ============================================================================

section_header(
    title="Executive Insights",
    description=(
        "Business observations derived from the current analytical outputs."
    ),
)


insight_columns = st.columns(
    3,
    gap="medium",
)


# ----------------------------------------------------------------------------
# Retention Insight
# ----------------------------------------------------------------------------

with insight_columns[0]:

    if (
        executive_kpis[
            "repeat_customer_rate"
        ]
        < 0.20
    ):

        insight_card(
            label="RETENTION",
            title=(
                "Customer retention requires attention"
            ),
            description=(
                "The current repeat-customer rate indicates "
                "an opportunity to convert more one-time buyers "
                "into returning customers."
            ),
            insight_type="danger",
        )

    else:

        insight_card(
            label="RETENTION",
            title=(
                "Repeat customer activity is relatively strong"
            ),
            description=(
                "The current customer base demonstrates a "
                "meaningful level of repeat purchasing."
            ),
            insight_type="success",
        )


# ----------------------------------------------------------------------------
# Customer Satisfaction Insight
# ----------------------------------------------------------------------------

with insight_columns[1]:

    if (
        executive_kpis[
            "low_review_rate"
        ]
        >= 0.15
    ):

        insight_card(
            label="CUSTOMER EXPERIENCE",
            title=(
                "Low-rated reviews require attention"
            ),
            description=(
                f"{executive_kpis['low_review_rate']:.1%} "
                "of valid reviews are rated 1 or 2, indicating "
                "a meaningful customer-experience risk."
            ),
            insight_type="warning",
        )

    else:

        insight_card(
            label="CUSTOMER EXPERIENCE",
            title=(
                "Customer satisfaction remains favorable"
            ),
            description=(
                "The share of low-rated reviews remains "
                "relatively limited across the available data."
            ),
            insight_type="success",
        )


# ----------------------------------------------------------------------------
# Forecast Insight
# ----------------------------------------------------------------------------

with insight_columns[2]:

    if not forecast_df.empty:

        forecast_rows = (
            forecast_df.dropna(
                subset=[
                    "predicted_revenue"
                ]
            )
        )

        if not forecast_rows.empty:

            insight_card(
                label="FORECAST",
                title=(
                    "Revenue forecast is available"
                ),
                description=(
                    "The forecasting pipeline provides predicted "
                    "revenue together with confidence bounds for "
                    "forward-looking planning."
                ),
                insight_type="success",
            )

        else:

            insight_card(
                label="FORECAST",
                title=(
                    "Forecast data requires attention"
                ),
                description=(
                    "The forecast dataset is available, but no "
                    "valid predicted revenue values were found."
                ),
                insight_type="warning",
            )

    else:

        insight_card(
            label="FORECAST",
            title=(
                "Forecast data is unavailable"
            ),
            description=(
                "No revenue forecast records are currently "
                "available for executive analysis."
            ),
            insight_type="warning",
        )


# ============================================================================
# EXECUTIVE DATA EXPORT
# ============================================================================

section_header(
    title="Executive Data",
    description=(
        "Download the transformed business-performance dataset."
    ),
)


export_buttons(
    dataframe=monthly_business,
    filename_prefix="executive_monthly_business",
    sheet_name="Monthly Business",
    key_prefix="executive_business_export",
)