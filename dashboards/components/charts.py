"""
Reusable chart components for the Enterprise Predictive Analytics Engine.

This module is the centralized visualization layer for the dashboard.

Responsibilities
----------------
- Create reusable Plotly visualizations.
- Apply consistent dashboard styling.
- Keep chart configuration out of individual pages.
- Handle empty and invalid datasets safely.
- Prevent large datasets from overwhelming the browser.
- Use SVG-based charts for maximum browser compatibility.
- Standardize titles, spacing, grids, hover behavior, and legends.

Architecture
------------
Pages
    ↓
Transformation layer
    ↓
Chart components
    ↓
Plotly / Streamlit

Business logic and data loading do not belong in this module.
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

PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#7C3AED"
SUCCESS_COLOR = "#059669"
WARNING_COLOR = "#D97706"
DANGER_COLOR = "#DC2626"
NEUTRAL_COLOR = "#64748B"

GRID_COLOR = "#E5E7EB"
TEXT_COLOR = "#0F172A"
MUTED_TEXT_COLOR = "#64748B"

WHITE = "#FFFFFF"
TRANSPARENT = "rgba(0,0,0,0)"


# ============================================================================
# CHART DEFAULTS
# ============================================================================

DEFAULT_CHART_HEIGHT = 380

DEFAULT_MARGIN = {
    "l": 55,
    "r": 25,
    "t": 55,
    "b": 50,
}

# Maximum number of customer observations rendered in scatter plots.
MAX_SCATTER_POINTS = 6000


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def _validate_dataframe(
    dataframe: pd.DataFrame,
) -> bool:
    """
    Check whether the supplied dataframe is usable for visualization.
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
    Validate that all required columns exist in the dataframe.
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
    Render a consistent empty-state message.
    """

    st.info(
        message,
        icon="ℹ️",
    )


# ============================================================================
# SCATTER DATA PREPARATION
# ============================================================================

def _prepare_scatter_data(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    max_points: int = MAX_SCATTER_POINTS,
) -> pd.DataFrame:
    """
    Prepare customer-level data for browser-safe scatter rendering.

    Large customer datasets are sampled deterministically so that the
    browser does not have to render tens of thousands of points.
    """

    columns_to_keep = [x, y]

    if color:
        columns_to_keep.append(color)

    prepared = dataframe[columns_to_keep].copy()

    # Remove observations that cannot be plotted.
    prepared = prepared.dropna(
        subset=[x, y]
    )

    if prepared.empty:
        return prepared

    # No sampling is necessary for reasonably small datasets.
    if len(prepared) <= max_points:
        return prepared.reset_index(drop=True)

    # ------------------------------------------------------------------------
    # Preserve high-value / extreme observations.
    # ------------------------------------------------------------------------

    extreme_count = min(
        500,
        max_points // 5,
    )

    extreme_indices: set[int] = set()

    try:
        x_numeric = pd.to_numeric(
            prepared[x],
            errors="coerce",
        )

        y_numeric = pd.to_numeric(
            prepared[y],
            errors="coerce",
        )

        extreme_x = (
            x_numeric
            .nlargest(extreme_count)
            .index
        )

        extreme_y = (
            y_numeric
            .nlargest(extreme_count)
            .index
        )

        extreme_indices.update(
            extreme_x.tolist()
        )

        extreme_indices.update(
            extreme_y.tolist()
        )

    except Exception:
        extreme_indices = set()

    extreme_indices = set(
        list(extreme_indices)[: max_points // 4]
    )

    remaining = prepared.drop(
        index=list(extreme_indices),
        errors="ignore",
    )

    remaining_slots = max_points - len(
        extreme_indices
    )

    # ------------------------------------------------------------------------
    # Category-aware sampling.
    # ------------------------------------------------------------------------

    sampled_parts = []

    if color and color in remaining.columns:

        category_count = remaining[color].nunique(
            dropna=True
        )

        if category_count > 0:

            per_category = max(
                1,
                remaining_slots // category_count,
            )

            for _, group in remaining.groupby(
                color,
                dropna=False,
            ):

                sample_size = min(
                    len(group),
                    per_category,
                )

                if sample_size > 0:

                    sampled_parts.append(
                        group.sample(
                            n=sample_size,
                            random_state=42,
                        )
                    )

    if sampled_parts:

        sampled = pd.concat(
            sampled_parts,
            ignore_index=False,
        )

    else:

        sampled = remaining.sample(
            n=min(
                remaining_slots,
                len(remaining),
            ),
            random_state=42,
        )

    # Fill remaining space if category-aware sampling did not
    # reach the target size.
    if len(sampled) < remaining_slots:

        sampled_indices = set(
            sampled.index
        )

        additional = remaining.drop(
            index=list(sampled_indices),
            errors="ignore",
        )

        additional_count = min(
            remaining_slots - len(sampled),
            len(additional),
        )

        if additional_count > 0:

            sampled = pd.concat(
                [
                    sampled,
                    additional.sample(
                        n=additional_count,
                        random_state=42,
                    ),
                ]
            )

    # ------------------------------------------------------------------------
    # Combine extreme observations and sampled observations.
    # ------------------------------------------------------------------------

    if extreme_indices:

        extreme_rows = prepared.loc[
            prepared.index.intersection(
                extreme_indices
            )
        ]

        sampled = pd.concat(
            [
                extreme_rows,
                sampled,
            ]
        )

    sampled = (
        sampled
        .loc[
            ~sampled.index.duplicated(
                keep="first"
            )
        ]
        .head(max_points)
        .reset_index(drop=True)
    )

    return sampled


# ============================================================================
# COMMON LAYOUT
# ============================================================================

def _base_layout(
    title: Optional[str] = None,
    height: int = DEFAULT_CHART_HEIGHT,
) -> dict:
    """
    Return the shared dashboard Plotly layout.
    """

    title_config = None

    if title:

        title_config = {
            "text": title,
            "x": 0,
            "xanchor": "left",
            "y": 0.98,
            "yanchor": "top",
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
            "size": 12,
        },

        "hoverlabel": {
            "bgcolor": WHITE,
            "bordercolor": GRID_COLOR,
            "font": {
                "size": 12,
                "color": TEXT_COLOR,
            },
        },

        "legend": {
            "font": {
                "size": 11,
                "color": MUTED_TEXT_COLOR,
            },
            "bgcolor": TRANSPARENT,
        },

        "hovermode": "closest",
    }


# ============================================================================
# AXIS STYLING
# ============================================================================

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
        gridwidth=1,
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
        automargin=True,
    )

    figure.update_yaxes(
        title=y_title,
        showgrid=show_y_grid,
        gridcolor=GRID_COLOR,
        gridwidth=1,
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
        automargin=True,
    )


# ============================================================================
# FIGURE RENDERING
# ============================================================================

def _render_figure(
    figure: go.Figure,
) -> None:
    """
    Render a Plotly figure using SVG-compatible rendering.

    SVG is deliberately used instead of WebGL because the dashboard
    should work reliably across browsers, remote desktops and machines
    where WebGL support is unavailable.
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
    Render a reusable SVG-based line chart.
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
        render_mode="svg",
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

    if color is None:

        figure.update_traces(
            marker_color=PRIMARY_COLOR,
            marker_line_width=0,
        )

    if text:

        figure.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
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
        show_y_grid=True,
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
    Render a reusable horizontal ranking chart.
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
        marker_line_width=0,
    )

    if text:

        figure.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
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
    Render a reusable area chart.
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
        render_mode="svg",
    )

    figure.update_traces(
        line={
            "color": PRIMARY_COLOR,
            "width": 2,
        },
        fillcolor="rgba(37,99,235,0.10)",
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
        marker={
            "line": {
                "color": WHITE,
                "width": 2,
            }
        },
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
                "color": MUTED_TEXT_COLOR,
            },
            "bgcolor": TRANSPARENT,
        }
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
    opacity: float = 0.65,
) -> None:
    """
    Render a browser-safe SVG scatter chart.

    Important
    ---------
    This function intentionally uses graph_objects.Scatter instead
    of Plotly Express scatter.

    That removes the WebGL dependency that was causing:

        "WebGL is not supported by your browser"

    The chart remains SVG-based even for customer-level data.
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

    plot_dataframe = _prepare_scatter_data(
        dataframe=dataframe,
        x=x,
        y=y,
        color=color,
        max_points=MAX_SCATTER_POINTS,
    )

    if plot_dataframe.empty:

        _render_empty_state(
            "No valid observations are available for this chart."
        )

        return

    figure = go.Figure()

    # ------------------------------------------------------------------------
    # SINGLE-CATEGORY SCATTER
    # ------------------------------------------------------------------------

    if not color:

        marker_size = 7

        if size:

            numeric_size = pd.to_numeric(
                plot_dataframe[size],
                errors="coerce",
            )

            if numeric_size.notna().any():

                normalized_size = (
                    numeric_size
                    .fillna(numeric_size.median())
                    .clip(lower=0)
                )

                max_size = normalized_size.max()

                if max_size > 0:

                    marker_size = (
                        5
                        + (
                            normalized_size
                            / max_size
                        ) * 12
                    )

        figure.add_trace(
            go.Scatter(
                x=plot_dataframe[x],
                y=plot_dataframe[y],
                mode="markers",
                marker={
                    "size": marker_size,
                    "color": PRIMARY_COLOR,
                    "opacity": opacity,
                    "line": {
                        "width": 0.5,
                        "color": WHITE,
                    },
                },
                name="Customers",
                hovertemplate=(
                    f"<b>{x}</b>: "
                    "%{x}<br>"
                    f"<b>{y}</b>: "
                    "%{y}"
                    "<extra></extra>"
                ),
            )
        )

    # ------------------------------------------------------------------------
    # CATEGORY-BASED SCATTER
    # ------------------------------------------------------------------------

    else:

        categories = (
            plot_dataframe[color]
            .dropna()
            .unique()
            .tolist()
        )

        category_palette = [
            PRIMARY_COLOR,
            SECONDARY_COLOR,
            SUCCESS_COLOR,
            WARNING_COLOR,
            DANGER_COLOR,
            "#0891B2",
            "#DB2777",
            "#4F46E5",
        ]

        for index, category in enumerate(categories):

            category_df = plot_dataframe[
                plot_dataframe[color] == category
            ]

            figure.add_trace(
                go.Scatter(
                    x=category_df[x],
                    y=category_df[y],
                    mode="markers",
                    name=str(category),
                    marker={
                        "size": 7,
                        "color": category_palette[
                            index % len(category_palette)
                        ],
                        "opacity": opacity,
                        "line": {
                            "width": 0.5,
                            "color": WHITE,
                        },
                    },
                    hovertemplate=(
                        f"<b>{color}</b>: "
                        f"{category}"
                        "<br>"
                        f"<b>{x}</b>: "
                        "%{x}"
                        "<br>"
                        f"<b>{y}</b>: "
                        "%{y}"
                        "<extra></extra>"
                    ),
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

    if color:

        figure.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "left",
                "x": 0,
                "font": {
                    "size": 11,
                    "color": MUTED_TEXT_COLOR,
                },
                "bgcolor": TRANSPARENT,
            }
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
    Render a reusable histogram.
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
        marker_line_width=0,
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

    Confidence intervals are rendered behind the forecast line.
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

    df = df.dropna(
        subset=[date_column]
    )

    df = df.sort_values(
        date_column
    )

    if df.empty:

        _render_empty_state(
            "No valid forecast observations are available."
        )

        return

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
            hovertemplate=(
                "<b>Actual</b><br>"
                "%{x|%b %Y}<br>"
                "%{y:,.0f}"
                "<extra></extra>"
            ),
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
            hovertemplate=(
                "<b>Forecast</b><br>"
                "%{x|%b %Y}<br>"
                "%{y:,.0f}"
                "<extra></extra>"
            ),
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
            "font": {
                "size": 11,
                "color": MUTED_TEXT_COLOR,
            },
            "bgcolor": TRANSPARENT,
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