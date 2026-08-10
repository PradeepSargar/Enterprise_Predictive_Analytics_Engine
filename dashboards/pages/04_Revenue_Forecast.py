"""
Revenue Forecast Dashboard.

This page presents historical revenue alongside future forecasted
revenue and forecast confidence intervals.

Responsibilities
----------------
1. Load prepared revenue forecast data.
2. Use the transformation layer to prepare dashboard metrics.
3. Present forecast KPIs.
4. Visualize actual versus forecast revenue.
5. Present forecast growth and forecast horizon.
6. Present forecast confidence information.
7. Provide a detailed forecast table.

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
    bar_chart,
    forecast_chart,
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
# DATA CLEANUP
# ============================================================================

forecast_df = forecast_df.copy()


# Convert date column safely.

forecast_df["month"] = pd.to_datetime(
    forecast_df["month"],
    errors="coerce",
)


# Convert financial values to numeric.

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


# Remove rows without a valid date.

forecast_df = forecast_df.dropna(
    subset=["month"]
)


# Sort chronologically.

forecast_df = (
    forecast_df
    .sort_values("month")
    .reset_index(drop=True)
)


if forecast_df.empty:

    st.warning(
        "No valid dated forecast observations are available."
    )

    st.stop()


# ============================================================================
# IDENTIFY HISTORICAL AND FUTURE PERIODS
# ============================================================================
#
# A forecast dataset may contain model predictions for historical periods
# as well as predictions for future periods.
#
# Therefore:
#
#   actual_revenue available
#       -> historical / observed period
#
#   actual_revenue missing + predicted_revenue available
#       -> future forecast period
#
# This prevents historical fitted predictions from being incorrectly
# counted as future forecast revenue.

historical_df = (
    forecast_df[
        forecast_df["actual_revenue"].notna()
    ]
    .copy()
)


future_forecast_df = (
    forecast_df[
        forecast_df["actual_revenue"].isna()
        & forecast_df["predicted_revenue"].notna()
    ]
    .copy()
)


# ============================================================================
# FALLBACK FOR DATASETS WITHOUT EXPLICIT FUTURE ROWS
# ============================================================================
#
# Some forecast files contain predictions for every period but do not leave
# actual_revenue blank for future periods.
#
# In that case, use the last observed actual period as the historical
# boundary and treat later prediction periods as future forecasts.

if future_forecast_df.empty:

    if not historical_df.empty:

        last_actual_month = (
            historical_df["month"]
            .max()
        )

        future_forecast_df = (
            forecast_df[
                (
                    forecast_df["month"]
                    > last_actual_month
                )
                & forecast_df["predicted_revenue"].notna()
            ]
            .copy()
        )


# ============================================================================
# HISTORICAL METRICS
# ============================================================================

historical_revenue = (
    historical_df["actual_revenue"]
    .dropna()
)


if not historical_revenue.empty:

    total_actual_revenue = (
        historical_revenue.sum()
    )

    latest_actual_revenue = (
        historical_df
        .sort_values("month")
        ["actual_revenue"]
        .iloc[-1]
    )

else:

    total_actual_revenue = 0.0

    latest_actual_revenue = 0.0


# ============================================================================
# FUTURE FORECAST METRICS
# ============================================================================

future_revenue = (
    future_forecast_df["predicted_revenue"]
    .dropna()
)


if not future_revenue.empty:

    total_future_forecast = (
        future_revenue.sum()
    )

    final_forecast_revenue = (
        future_forecast_df
        .sort_values("month")
        ["predicted_revenue"]
        .iloc[-1]
    )

else:

    total_future_forecast = 0.0

    final_forecast_revenue = 0.0


# ============================================================================
# FORECAST HORIZON
# ============================================================================

forecast_periods = len(
    future_forecast_df
)


if not future_forecast_df.empty:

    forecast_start = (
        future_forecast_df["month"]
        .min()
    )

    forecast_end = (
        future_forecast_df["month"]
        .max()
    )

else:

    forecast_start = None
    forecast_end = None


# ============================================================================
# FORECAST GROWTH
# ============================================================================
#
# Compare the first future forecast period against the latest observed
# historical revenue.
#
# This is a directional forecast indicator rather than a historical
# year-over-year growth metric.

forecast_growth = None


if (
    latest_actual_revenue != 0
    and not future_forecast_df.empty
):

    first_forecast_revenue = (
        future_forecast_df
        .sort_values("month")
        ["predicted_revenue"]
        .iloc[0]
    )

    if pd.notna(first_forecast_revenue):

        forecast_growth = (
            (
                first_forecast_revenue
                - latest_actual_revenue
            )
            / latest_actual_revenue
        ) * 100


# ============================================================================
# FORECAST CONFIDENCE RANGE
# ============================================================================

if not future_forecast_df.empty:

    future_forecast_df["forecast_range"] = (
        future_forecast_df["upper_bound"]
        - future_forecast_df["lower_bound"]
    )

    average_forecast_range = (
        future_forecast_df["forecast_range"]
        .dropna()
        .mean()
    )

else:

    average_forecast_range = None


# ============================================================================
# FORECAST OVERVIEW
# ============================================================================

section_header(
    title="Forecast Overview",
    description=(
        "Key indicators summarizing observed revenue and the future "
        "forecast horizon."
    ),
)


kpi_columns = st.columns(
    4,
    gap="large",
)


# ----------------------------------------------------------------------------
# Historical Revenue
# ----------------------------------------------------------------------------

with kpi_columns[0]:

    kpi_card(
        label="Historical Revenue",
        value=f"₹{total_actual_revenue:,.0f}",
        delta="Observed revenue",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Future Forecast
# ----------------------------------------------------------------------------

with kpi_columns[1]:

    kpi_card(
        label="Future Forecast",
        value=f"₹{total_future_forecast:,.0f}",
        delta="Expected future revenue",
        delta_type="positive",
    )


# ----------------------------------------------------------------------------
# Forecast Growth
# ----------------------------------------------------------------------------

with kpi_columns[2]:

    if forecast_growth is None:

        growth_value = "N/A"
        growth_type = "neutral"

    elif forecast_growth >= 0:

        growth_value = f"{forecast_growth:+.1f}%"
        growth_type = "positive"

    else:

        growth_value = f"{forecast_growth:+.1f}%"
        growth_type = "negative"


    kpi_card(
        label="Forecast Growth",
        value=growth_value,
        delta="First forecast vs latest actual",
        delta_type=growth_type,
    )


# ----------------------------------------------------------------------------
# Forecast Horizon
# ----------------------------------------------------------------------------

with kpi_columns[3]:

    kpi_card(
        label="Forecast Periods",
        value=f"{forecast_periods:,}",
        delta="Future periods available",
        delta_type="neutral",
    )


# ============================================================================
# ACTUAL VS FORECAST TREND
# ============================================================================

section_header(
    title="Revenue Forecast Trend",
    description=(
        "Historical revenue, model forecast, and confidence interval "
        "across the available timeline."
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
# FUTURE FORECAST ANALYSIS
# ============================================================================

section_header(
    title="Future Forecast Analysis",
    description=(
        "Expected revenue across the future forecast horizon."
    ),
)


if future_forecast_df.empty:

    st.info(
        "No explicit future forecast periods were identified "
        "in the available forecast dataset."
    )

else:

    forecast_chart_df = (
        future_forecast_df[
            [
                "month",
                "predicted_revenue",
            ]
        ]
        .copy()
    )

    forecast_chart_df["period"] = (
        forecast_chart_df["month"]
        .dt.strftime("%b %Y")
    )


    bar_chart(
        dataframe=forecast_chart_df,
        x="period",
        y="predicted_revenue",
        title="Expected Revenue by Forecast Period",
        x_title="Forecast Period",
        y_title="Predicted Revenue",
        height=400,
        text=False,
    )


# ============================================================================
# FORECAST CONFIDENCE
# ============================================================================

section_header(
    title="Forecast Confidence",
    description=(
        "The confidence interval represents the expected range around "
        "each future revenue prediction."
    ),
)


confidence_columns = st.columns(
    3,
    gap="large",
)


# ----------------------------------------------------------------------------
# Average Range
# ----------------------------------------------------------------------------

with confidence_columns[0]:

    if average_forecast_range is not None:

        range_value = (
            f"₹{average_forecast_range:,.0f}"
        )

    else:

        range_value = "N/A"


    kpi_card(
        label="Average Forecast Range",
        value=range_value,
        delta="Average upper-to-lower interval",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Forecast Start
# ----------------------------------------------------------------------------

with confidence_columns[1]:

    if forecast_start is not None:

        start_value = (
            forecast_start.strftime("%b %Y")
        )

    else:

        start_value = "N/A"


    kpi_card(
        label="Forecast Start",
        value=start_value,
        delta="First future period",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# Forecast End
# ----------------------------------------------------------------------------

with confidence_columns[2]:

    if forecast_end is not None:

        end_value = (
            forecast_end.strftime("%b %Y")
        )

    else:

        end_value = "N/A"


    kpi_card(
        label="Forecast End",
        value=end_value,
        delta="Last future period",
        delta_type="neutral",
    )


# ============================================================================
# FORECAST DETAIL
# ============================================================================

section_header(
    title="Forecast Detail",
    description=(
        "Detailed future-period predictions and confidence bounds."
    ),
)


if future_forecast_df.empty:

    st.info(
        "There are no explicit future forecast records to display."
    )

else:

    detail_df = (
        future_forecast_df[
            [
                "month",
                "predicted_revenue",
                "lower_bound",
                "upper_bound",
            ]
        ]
        .copy()
    )


    detail_df = detail_df.rename(
        columns={
            "month": "Month",
            "predicted_revenue": "Forecast Revenue",
            "lower_bound": "Lower Bound",
            "upper_bound": "Upper Bound",
        }
    )


    detail_df["Month"] = (
        pd.to_datetime(
            detail_df["Month"],
            errors="coerce",
        )
        .dt.strftime("%b %Y")
    )


    st.dataframe(
        detail_df,
        use_container_width=True,
        hide_index=True,
        height=320,
        column_config={

            "Month": st.column_config.TextColumn(
                "Month",
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
        "Latest observed revenue compared with the first and final "
        "future forecast periods."
    ),
)


summary_columns = st.columns(
    3,
    gap="large",
)


# ----------------------------------------------------------------------------
# Latest Actual
# ----------------------------------------------------------------------------

with summary_columns[0]:

    kpi_card(
        label="Latest Actual Revenue",
        value=f"₹{latest_actual_revenue:,.2f}",
        delta="Most recent observed period",
        delta_type="neutral",
    )


# ----------------------------------------------------------------------------
# First Forecast
# ----------------------------------------------------------------------------

with summary_columns[1]:

    if not future_forecast_df.empty:

        first_forecast = (
            future_forecast_df
            .sort_values("month")
            ["predicted_revenue"]
            .iloc[0]
        )

        first_forecast_value = (
            f"₹{first_forecast:,.2f}"
        )

    else:

        first_forecast_value = "N/A"


    kpi_card(
        label="First Forecast",
        value=first_forecast_value,
        delta="First future prediction",
        delta_type="positive",
    )


# ----------------------------------------------------------------------------
# Final Forecast
# ----------------------------------------------------------------------------

with summary_columns[2]:

    kpi_card(
        label="Final Forecast",
        value=f"₹{final_forecast_revenue:,.2f}",
        delta="Last future prediction",
        delta_type="positive",
    )