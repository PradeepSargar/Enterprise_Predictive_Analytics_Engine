"""
Revenue Forecast Dashboard.

This page presents historical revenue alongside forecasted revenue
and confidence intervals.

Responsibilities
----------------
1. Load prepared revenue forecast data.
2. Use the transformation layer to prepare dashboard metrics.
3. Present forecast KPIs.
4. Visualize actual versus forecast revenue.
5. Present forecast growth and forecast horizon.
6. Provide a detailed monthly forecast table.

Architecture
------------
Data loading:
    dashboards.data.loader

Business transformations:
    dashboards.data.transformations

Visualization:
    dashboards.components.charts

Reusable UI:
    dashboards.components.kpi_cards
    dashboards.components.section_headers

No model training or business logic is performed directly in this page.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# DATA LAYER
# ============================================================================

from dashboards.data.loader import (
    load_revenue_forecast,
)


# ============================================================================
# TRANSFORMATION LAYER
# ============================================================================

from dashboards.data.transformations import (
    prepare_revenue_forecast,
)


# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

from dashboards.components.charts import (
    forecast_chart,
    bar_chart,
)

from dashboards.components.kpi_cards import (
    kpi_card,
)

from dashboards.components.section_headers import (
    page_header,
    section_header,
)


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="Revenue Forecast",
    description=(
        "Monitor historical revenue and evaluate expected future "
        "revenue using the forecasting model."
    ),
)


# ============================================================================
# LOAD FORECAST DATA
# ============================================================================

try:

    forecast_data = load_revenue_forecast()

except FileNotFoundError as exc:

    st.error(
        "Revenue forecast data could not be found."
    )

    st.caption(str(exc))

    st.stop()

except Exception as exc:

    st.error(
        "An unexpected error occurred while loading revenue "
        "forecast data."
    )

    st.caption(str(exc))

    st.stop()


# ============================================================================
# VALIDATE RAW DATA
# ============================================================================

if forecast_data is None or forecast_data.empty:

    st.warning(
        "Revenue forecast data is currently unavailable."
    )

    st.stop()


# ============================================================================
# PREPARE FORECAST DATA
# ============================================================================

try:

    forecast_df = prepare_revenue_forecast(
        forecast_data
    )

except Exception as exc:

    st.error(
        "Revenue forecast data could not be prepared."
    )

    st.caption(str(exc))

    st.stop()


# ============================================================================
# VALIDATE PREPARED DATA
# ============================================================================

required_columns = {
    "month",
    "predicted_revenue",
    "lower_bound",
    "upper_bound",
    "actual_revenue",
}


missing_columns = (
    required_columns
    - set(forecast_df.columns)
)


if missing_columns:

    st.error(
        "Prepared forecast data is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )

    st.stop()


if forecast_df.empty:

    st.warning(
        "No valid revenue forecast observations are available."
    )

    st.stop()


# ============================================================================
# NUMERIC CLEANUP
# ============================================================================

numeric_columns = [
    "predicted_revenue",
    "lower_bound",
    "upper_bound",
    "actual_revenue",
]


for column in numeric_columns:

    forecast_df[column] = pd.to_numeric(
        forecast_df[column],
        errors="coerce",
    )


forecast_df = forecast_df.sort_values(
    "month"
).reset_index(
    drop=True
)


# ============================================================================
# FORECAST METRICS
# ============================================================================

# Historical actual revenue.

actual_revenue = (
    forecast_df["actual_revenue"]
    .dropna()
)


# Forecasted revenue.

predicted_revenue = (
    forecast_df["predicted_revenue"]
    .dropna()
)


# ---------------------------------------------------------------------------
# Historical revenue
# ---------------------------------------------------------------------------

if not actual_revenue.empty:

    total_actual_revenue = (
        actual_revenue.sum()
    )

else:

    total_actual_revenue = 0.0


# ---------------------------------------------------------------------------
# Forecast revenue
# ---------------------------------------------------------------------------

if not predicted_revenue.empty:

    total_forecast_revenue = (
        predicted_revenue.sum()
    )

else:

    total_forecast_revenue = 0.0


# ---------------------------------------------------------------------------
# Forecast growth
# ---------------------------------------------------------------------------
#
# Compare the first available actual revenue period with the final
# predicted revenue period.
#
# This provides a simple directional indicator for the dashboard.

valid_actual = (
    forecast_df[
        forecast_df["actual_revenue"].notna()
    ]
    .sort_values("month")
)


valid_forecast = (
    forecast_df[
        forecast_df["predicted_revenue"].notna()
    ]
    .sort_values("month")
)


forecast_growth = None


if (
    not valid_actual.empty
    and not valid_forecast.empty
):

    baseline_revenue = (
        valid_actual["actual_revenue"]
        .iloc[-1]
    )

    final_forecast_revenue = (
        valid_forecast["predicted_revenue"]
        .iloc[-1]
    )

    if (
        pd.notna(baseline_revenue)
        and baseline_revenue != 0
        and pd.notna(final_forecast_revenue)
    ):

        forecast_growth = (
            (
                final_forecast_revenue
                - baseline_revenue
            )
            / baseline_revenue
        ) * 100


# ---------------------------------------------------------------------------
# Forecast periods
# ---------------------------------------------------------------------------

forecast_periods = (
    len(valid_forecast)
)


# ---------------------------------------------------------------------------
# Latest actual revenue
# ---------------------------------------------------------------------------

if not valid_actual.empty:

    latest_actual_revenue = (
        valid_actual["actual_revenue"]
        .iloc[-1]
    )

else:

    latest_actual_revenue = 0.0


# ---------------------------------------------------------------------------
# Final forecast
# ---------------------------------------------------------------------------

if not valid_forecast.empty:

    final_forecast = (
        valid_forecast["predicted_revenue"]
        .iloc[-1]
    )

else:

    final_forecast = 0.0


# ============================================================================
# FORECAST OVERVIEW
# ============================================================================

section_header(
    title="Forecast Overview",
    description=(
        "Key revenue indicators from the historical and forecast periods."
    ),
)


kpi_columns = st.columns(
    4,
    gap="large",
)


# ----------------------------------------------------------------------------
# KPI 1
# ----------------------------------------------------------------------------

with kpi_columns[0]:

    kpi_card(
        label="Historical Revenue",
        value=f"₹{total_actual_revenue:,.0f}",
        delta="Observed revenue",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# KPI 2
# ----------------------------------------------------------------------------

with kpi_columns[1]:

    kpi_card(
        label="Forecast Revenue",
        value=f"₹{total_forecast_revenue:,.0f}",
        delta="Forecast-period revenue",
        delta_type="positive",
    )


# ----------------------------------------------------------------------------
# KPI 3
# ----------------------------------------------------------------------------

with kpi_columns[2]:

    if forecast_growth is not None:

        if forecast_growth >= 0:

            growth_delta_type = "positive"

        else:

            growth_delta_type = "negative"


        growth_value = (
            f"{forecast_growth:+.1f}%"
        )

    else:

        growth_delta_type = "neutral"

        growth_value = "N/A"


    kpi_card(
        label="Forecast Growth",
        value=growth_value,
        delta="Versus latest actual period",
        delta_type=growth_delta_type,
    )


# ----------------------------------------------------------------------------
# KPI 4
# ----------------------------------------------------------------------------

with kpi_columns[3]:

    kpi_card(
        label="Forecast Periods",
        value=f"{forecast_periods:,}",
        delta="Available forecast periods",
        delta_type="neutral",
    )


# ============================================================================
# ACTUAL VS FORECAST
# ============================================================================

section_header(
    title="Revenue Forecast Trend",
    description=(
        "Historical actual revenue compared with model-predicted revenue "
        "and the forecast confidence interval."
    ),
)


forecast_chart(
    dataframe=forecast_df,
    date_column="month",
    actual_column="actual_revenue",
    forecast_column="predicted_revenue",
    lower_column="lower_bound",
    upper_column="upper_bound",
    title="Actual vs Forecast Revenue",
    x_title="Month",
    y_title="Revenue",
    height=450,
)


# ============================================================================
# FORECAST PERIOD ANALYSIS
# ============================================================================

section_header(
    title="Forecast Period Analysis",
    description=(
        "Expected revenue across the available forecast horizon."
    ),
)


# Create a dedicated dataframe for the forecast periods.

forecast_period_df = (
    forecast_df[
        forecast_df["predicted_revenue"].notna()
    ]
    .copy()
)


if forecast_period_df.empty:

    st.info(
        "No forecast-period observations are available."
    )

else:

    forecast_period_df["period"] = (
        forecast_period_df["month"]
        .dt.strftime("%b %Y")
    )


    bar_chart(
        dataframe=forecast_period_df,
        x="period",
        y="predicted_revenue",
        title="Forecast Revenue by Period",
        x_title="Forecast Period",
        y_title="Predicted Revenue",
        height=400,
        text=False,
    )


# ============================================================================
# CONFIDENCE INTERVAL ANALYSIS
# ============================================================================

section_header(
    title="Forecast Confidence",
    description=(
        "Upper and lower bounds indicate the expected range around "
        "the model forecast."
    ),
)


confidence_df = (
    forecast_df[
        [
            "month",
            "predicted_revenue",
            "lower_bound",
            "upper_bound",
        ]
    ]
    .copy()
)


confidence_df["Forecast Range"] = (
    confidence_df["upper_bound"]
    - confidence_df["lower_bound"]
)


average_forecast_range = (
    confidence_df["Forecast Range"]
    .dropna()
    .mean()
)


if pd.notna(average_forecast_range):

    kpi_card(
        label="Average Forecast Range",
        value=f"₹{average_forecast_range:,.0f}",
        delta="Average upper-to-lower interval",
        delta_type="neutral",
    )

else:

    kpi_card(
        label="Average Forecast Range",
        value="N/A",
        delta="Confidence interval unavailable",
        delta_type="neutral",
    )


# ============================================================================
# FORECAST DETAIL
# ============================================================================

section_header(
    title="Forecast Detail",
    description=(
        "Detailed monthly actual, forecast, and confidence-bound values."
    ),
)


detail_df = forecast_df[
    [
        "month",
        "actual_revenue",
        "predicted_revenue",
        "lower_bound",
        "upper_bound",
    ]
].copy()


# ----------------------------------------------------------------------------
# Rename columns
# ----------------------------------------------------------------------------

detail_df = detail_df.rename(
    columns={
        "month": "Month",
        "actual_revenue": "Actual Revenue",
        "predicted_revenue": "Forecast Revenue",
        "lower_bound": "Lower Bound",
        "upper_bound": "Upper Bound",
    }
)


# ----------------------------------------------------------------------------
# Format month
# ----------------------------------------------------------------------------

detail_df["Month"] = (
    pd.to_datetime(
        detail_df["Month"],
        errors="coerce",
    )
    .dt.strftime("%b %Y")
)


# ----------------------------------------------------------------------------
# Native Streamlit table
# ----------------------------------------------------------------------------
#
# Native Streamlit rendering is intentionally used instead of custom HTML.
# This prevents the HTML rendering problem encountered elsewhere in the
# dashboard.

st.dataframe(
    detail_df,
    use_container_width=True,
    hide_index=True,
    height=300,
    column_config={

        "Month": st.column_config.TextColumn(
            "Month",
            width="medium",
        ),

        "Actual Revenue": st.column_config.NumberColumn(
            "Actual Revenue",
            format="₹%.2f",
            width="medium",
        ),

        "Forecast Revenue": st.column_config.NumberColumn(
            "Forecast Revenue",
            format="₹%.2f",
            width="medium",
        ),

        "Lower Bound": st.column_config.NumberColumn(
            "Lower Bound",
            format="₹%.2f",
            width="medium",
        ),

        "Upper Bound": st.column_config.NumberColumn(
            "Upper Bound",
            format="₹%.2f",
            width="medium",
        ),
    },
)


# ============================================================================
# FORECAST SUMMARY
# ============================================================================

section_header(
    title="Forecast Summary",
    description=(
        "Summary of the latest observed revenue and the final forecast."
    ),
)


summary_columns = st.columns(
    2,
    gap="large",
)


with summary_columns[0]:

    kpi_card(
        label="Latest Actual Revenue",
        value=f"₹{latest_actual_revenue:,.2f}",
        delta="Most recent observed period",
        delta_type="neutral",
    )


with summary_columns[1]:

    kpi_card(
        label="Final Forecast Revenue",
        value=f"₹{final_forecast:,.2f}",
        delta="Latest available forecast",
        delta_type="positive",
    )