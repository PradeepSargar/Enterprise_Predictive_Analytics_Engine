"""
Reusable chart components.

This module provides the centralized visualization layer for the
Enterprise Predictive Analytics Engine dashboard.

Responsibilities
----------------
- Create reusable Plotly visualizations.
- Apply consistent dashboard styling.
- Keep chart configuration out of individual pages.
- Provide safe handling for empty datasets.
- Standardize titles, spacing, grids, hover behavior, and legends.

The chart layer does NOT:
- load data
- calculate business metrics
- perform machine learning
- modify source DataFrames
- inject global CSS

Pages and transformation modules remain responsible for those concerns.
"""

from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================================
# DESIGN TOKENS
# ============================================================================

# These values intentionally remain local to the chart system.
# Global application colors can later be centralized in styles/colors.py.

PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#7C3AED"
SUCCESS_COLOR = "#059669"
WARNING_COLOR = "#D97706"
DANGER_COLOR = "#DC2626"
NEUTRAL_COLOR = "#64748B"

GRID_COLOR = "#E5E7EB"
TEXT_COLOR = "#0F172A"
MUTED_TEXT_COLOR = "#64748B"

TRANSPARENT = "rgba(0,0,0,0)"


# ============================================================================
# COMMON CHART CONFIGURATION
# ============================================================================

DEFAULT_CHART_HEIGHT = 380

DEFAULT_MARGIN = {
    "l": 10,
    "r": 25,
    "t": 55,
    "b": 15,
}


# ============================================================================
# INTERNAL HELPERS
# ============================================================================

def _validate_dataframe(
    dataframe: pd.DataFrame,
) -> bool:
    """
    Validate that a chart received a usable DataFrame.

    Returns
    -------
    bool
        True when the DataFrame contains usable rows.
    """

    if dataframe is None:
        return False

    if not isinstance(dataframe, pd.DataFrame):
        return False

    if dataframe.empty:
        return False

    return True


def _validate_columns(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> None:
    """
    Validate that required chart columns exist.

    Raises
    ------
    ValueError
        When one or more required columns are missing.
    """

    missing_columns = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        raise ValueError(
            "Chart data is missing required columns: "
            + ", ".join(missing_columns)
        )


def _render_empty_state(
    message: str,
) -> None:
    """
    Render a consistent empty-state message when chart data is unavailable.
    """

    st.info(
        message,
        icon="ℹ️",
    )


def _base_layout(
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> dict:
    """
    Return the shared Plotly layout configuration.

    Keeping this configuration centralized prevents each dashboard
    page from developing its own visual language.
    """

    title_config = None

    if title:

        title_config = {
            "text": title,
            "x": 0,
            "xanchor": "left",
            "font": {
                "size": 16,
                "color": TEXT_COLOR,
            },
        }

    return {
        "title": title_config,
        "height": height,
        "margin": DEFAULT_MARGIN.copy(),
        "paper_bgcolor": TRANSPARENT,
        "plot_bgcolor": TRANSPARENT,
        "font": {
            "family": (
                "Inter, -apple-system, BlinkMacSystemFont, "
                "Segoe UI, sans-serif"
            ),
            "color": MUTED_TEXT_COLOR,
        },
        "hoverlabel": {
            "font": {
                "size": 12,
            },
        },
        "legend": {
            "font": {
                "size": 11,
            },
        },
    }


def _apply_axis_style(
    figure: go.Figure,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    show_x_grid: bool = True,
    show_y_grid: bool = True,
) -> None:
    """
    Apply the standard dashboard axis styling.
    """

    figure.update_xaxes(
        title=x_title,
        showgrid=show_x_grid,
        gridcolor=GRID_COLOR,
        zeroline=False,
        showline=False,
        title_font={
            "size": 12,
            "color": MUTED_TEXT_COLOR,
        },
        tickfont={
            "size": 11,
            "color": MUTED_TEXT_COLOR,
        },
    )

    figure.update_yaxes(
        title=y_title,
        showgrid=show_y_grid,
        gridcolor=GRID_COLOR,
        zeroline=False,
        showline=False,
        title_font={
            "size": 12,
            "color": MUTED_TEXT_COLOR,
        },
        tickfont={
            "size": 11,
            "color": MUTED_TEXT_COLOR,
        },
    )


def _render_figure(
    figure: go.Figure,
) -> None:
    """
    Render a Plotly figure using dashboard-standard Streamlit settings.
    """

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ============================================================================
# LINE CHART
# ============================================================================

def line_chart(
    dataframe: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    markers: bool = True,
    color: Optional[str] = None,
) -> None:
    """
    Render a reusable line chart.

    Parameters
    ----------
    dataframe:
        Source DataFrame.

    x:
        Column used for the x-axis.

    y:
        Column or columns used for the y-axis.

    title:
        Optional chart title.

    x_title:
        Optional x-axis title.

    y_title:
        Optional y-axis title.

    height:
        Chart height in pixels.

    markers:
        Whether data-point markers should be displayed.

    color:
        Optional Plotly color column for multi-category lines.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    y_columns = (
        [y]
        if isinstance(y, str)
        else list(y)
    )

    required_columns = [
        x,
        *y_columns,
    ]

    if color:
        required_columns.append(color)

    _validate_columns(
        dataframe,
        required_columns,
    )

    figure = px.line(
        dataframe,
        x=x,
        y=y_columns,
        color=color,
        markers=markers,
    )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=x_title,
        y_title=y_title,
    )

    _render_figure(
        figure
    )


# ============================================================================
# BAR CHART
# ============================================================================

def bar_chart(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    color: Optional[str] = None,
    text: bool = False,
) -> None:
    """
    Render a reusable vertical bar chart.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    required_columns = [
        x,
        y,
    ]

    if color:
        required_columns.append(color)

    _validate_columns(
        dataframe,
        required_columns,
    )

    figure = px.bar(
        dataframe,
        x=x,
        y=y,
        color=color,
        text=y if text else None,
    )

    figure.update_traces(
        marker_color=(
            PRIMARY_COLOR
            if color is None
            else None
        ),
    )

    if text:

        figure.update_traces(
            texttemplate="%{text}",
            textposition="outside",
        )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=x_title,
        y_title=y_title,
    )

    _render_figure(
        figure
    )


# ============================================================================
# HORIZONTAL BAR CHART
# ============================================================================

def horizontal_bar_chart(
    dataframe: pd.DataFrame,
    category: str,
    value: str,
    title: Optional[str] = None,
    category_title: Optional[str] = None,
    value_title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    text: bool = False,
) -> None:
    """
    Render a reusable horizontal bar chart.

    Particularly useful for rankings and segment comparisons.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    _validate_columns(
        dataframe,
        [
            category,
            value,
        ],
    )

    figure = px.bar(
        dataframe,
        x=value,
        y=category,
        orientation="h",
        text=value if text else None,
    )

    figure.update_traces(
        marker_color=PRIMARY_COLOR,
    )

    if text:

        figure.update_traces(
            texttemplate="%{text}",
            textposition="outside",
        )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=value_title,
        y_title=category_title,
        show_x_grid=True,
        show_y_grid=False,
    )

    _render_figure(
        figure
    )


# ============================================================================
# AREA CHART
# ============================================================================

def area_chart(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> None:
    """
    Render a reusable area chart for volume and trend analysis.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    _validate_columns(
        dataframe,
        [
            x,
            y,
        ],
    )

    figure = px.area(
        dataframe,
        x=x,
        y=y,
    )

    figure.update_traces(
        line={
            "color": PRIMARY_COLOR,
        },
    )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=x_title,
        y_title=y_title,
    )

    _render_figure(
        figure
    )


# ============================================================================
# DONUT CHART
# ============================================================================

def donut_chart(
    dataframe: pd.DataFrame,
    names: str,
    values: str,
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    hole: float = 0.62,
) -> None:
    """
    Render a reusable donut chart.

    Best suited to small part-to-whole comparisons such as
    customer segment composition.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    _validate_columns(
        dataframe,
        [
            names,
            values,
        ],
    )

    figure = px.pie(
        dataframe,
        names=names,
        values=values,
        hole=hole,
    )

    figure.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Value: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
    )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    figure.update_layout(
        legend={
            "orientation": "v",
            "font": {
                "size": 11,
            },
        },
    )

    _render_figure(
        figure
    )


# ============================================================================
# SCATTER CHART
# ============================================================================

def scatter_chart(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
    opacity: float = 0.7,
) -> None:
    """
    Render a reusable scatter chart.

    Useful for relationship analysis such as:

    - Frequency vs monetary value
    - Sales vs profit
    - Risk probability vs customer value
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    required_columns = [
        x,
        y,
    ]

    if color:
        required_columns.append(color)

    if size:
        required_columns.append(size)

    _validate_columns(
        dataframe,
        required_columns,
    )

    figure = px.scatter(
        dataframe,
        x=x,
        y=y,
        color=color,
        size=size,
        opacity=opacity,
    )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=x_title,
        y_title=y_title,
    )

    _render_figure(
        figure
    )


# ============================================================================
# HISTOGRAM
# ============================================================================

def histogram(
    dataframe: pd.DataFrame,
    column: str,
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: str = "Count",
    bins: int = 30,
    height: int = DEFAULT_CHART_HEIGHT,
    color: str = PRIMARY_COLOR,
) -> None:
    """
    Render a reusable histogram for distribution analysis.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this chart."
        )

        return

    _validate_columns(
        dataframe,
        [
            column,
        ],
    )

    figure = px.histogram(
        dataframe,
        x=column,
        nbins=bins,
    )

    figure.update_traces(
        marker_color=color,
        hovertemplate=(
            "%{x}<br>"
            "Count: %{y:,}"
            "<extra></extra>"
        ),
    )

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=x_title,
        y_title=y_title,
    )

    _render_figure(
        figure
    )


# ============================================================================
# FORECAST CHART
# ============================================================================

def forecast_chart(
    dataframe: pd.DataFrame,
    date_column: str,
    actual_column: str,
    forecast_column: str,
    lower_column: Optional[str] = None,
    upper_column: Optional[str] = None,
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    height: int = 420,
) -> None:
    """
    Render a professional actual-vs-forecast chart.

    Parameters
    ----------
    dataframe:
        Forecast dataset.

    date_column:
        Time-axis column.

    actual_column:
        Historical/actual values.

    forecast_column:
        Forecast values.

    lower_column:
        Optional lower confidence bound.

    upper_column:
        Optional upper confidence bound.

    title:
        Chart title.

    x_title:
        X-axis title.

    y_title:
        Y-axis title.

    Notes
    -----
    Confidence intervals are rendered as a translucent area behind
    the forecast line.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No forecast data is available."
        )

        return

    required_columns = [
        date_column,
        actual_column,
        forecast_column,
    ]

    if lower_column:
        required_columns.append(
            lower_column
        )

    if upper_column:
        required_columns.append(
            upper_column
        )

    _validate_columns(
        dataframe,
        required_columns,
    )

    df = dataframe.copy()

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce",
    )

    df = df.sort_values(
        date_column
    )

    figure = go.Figure()


    # ------------------------------------------------------------------------
    # Confidence interval
    # ------------------------------------------------------------------------

    if lower_column and upper_column:

        figure.add_trace(
            go.Scatter(
                x=df[date_column],
                y=df[upper_column],
                mode="lines",
                line={
                    "width": 0,
                    "color": TRANSPARENT,
                },
                showlegend=False,
                hoverinfo="skip",
            )
        )

        figure.add_trace(
            go.Scatter(
                x=df[date_column],
                y=df[lower_column],
                mode="lines",
                line={
                    "width": 0,
                    "color": TRANSPARENT,
                },
                fill="tonexty",
                fillcolor="rgba(124,58,237,0.12)",
                name="Confidence interval",
                hoverinfo="skip",
            )
        )


    # ------------------------------------------------------------------------
    # Actual values
    # ------------------------------------------------------------------------

    figure.add_trace(
        go.Scatter(
            x=df[date_column],
            y=df[actual_column],
            mode="lines+markers",
            name="Actual",
            line={
                "color": NEUTRAL_COLOR,
                "width": 2,
            },
            marker={
                "size": 6,
            },
        )
    )


    # ------------------------------------------------------------------------
    # Forecast values
    # ------------------------------------------------------------------------

    figure.add_trace(
        go.Scatter(
            x=df[date_column],
            y=df[forecast_column],
            mode="lines+markers",
            name="Forecast",
            line={
                "color": SECONDARY_COLOR,
                "width": 3,
            },
            marker={
                "size": 6,
            },
        )
    )


    # ------------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------------

    figure.update_layout(
        **_base_layout(
            title=title,
            height=height,
        )
    )

    _apply_axis_style(
        figure,
        x_title=x_title,
        y_title=y_title,
    )

    figure.update_layout(
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        }
    )

    _render_figure(
        figure
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "line_chart",
    "bar_chart",
    "horizontal_bar_chart",
    "area_chart",
    "donut_chart",
    "scatter_chart",
    "histogram",
    "forecast_chart",
]