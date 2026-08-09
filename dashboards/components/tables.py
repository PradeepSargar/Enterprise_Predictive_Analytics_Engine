"""
Reusable table components for the dashboard.

This module provides the centralized table-rendering layer for the
Enterprise Predictive Analytics Engine.

Responsibilities
----------------
- Render consistent analytical tables.
- Provide safe handling of empty datasets.
- Standardize table height and width.
- Support ranking-oriented tables.
- Support model/comparison tables.
- Keep table presentation logic out of dashboard pages.

This module intentionally uses Streamlit's native dataframe rendering
instead of custom HTML tables. This provides better stability,
sorting, resizing, and compatibility with the Streamlit runtime.
"""

from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd
import streamlit as st


# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

DEFAULT_TABLE_HEIGHT = 420

DEFAULT_RANKED_HEIGHT = 380

DEFAULT_COMPARISON_HEIGHT = 360


# ============================================================================
# INTERNAL HELPERS
# ============================================================================

def _validate_dataframe(
    dataframe: pd.DataFrame | None,
) -> bool:
    """
    Check whether the supplied object is a usable DataFrame.

    Returns
    -------
    bool
        True when the object is a non-empty DataFrame.
    """

    return (
        dataframe is not None
        and isinstance(dataframe, pd.DataFrame)
        and not dataframe.empty
    )


def _render_empty_state(
    message: str,
) -> None:
    """
    Render a consistent message when table data is unavailable.
    """

    st.info(
        message,
        icon="ℹ️",
    )


def _validate_columns(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> None:
    """
    Validate that requested columns exist.

    Raises
    ------
    ValueError
        If one or more requested columns are missing.
    """

    missing_columns = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Table data is missing required columns: "
            + ", ".join(missing_columns)
        )


# ============================================================================
# GENERAL DATA TABLE
# ============================================================================

def render_data_table(
    dataframe: pd.DataFrame,
    columns: Optional[list[str]] = None,
    height: int = DEFAULT_TABLE_HEIGHT,
    hide_index: bool = True,
    use_container_width: bool = True,
    title: Optional[str] = None,
) -> None:
    """
    Render a general-purpose analytical table.

    Parameters
    ----------
    dataframe:
        DataFrame containing the table data.

    columns:
        Optional list of columns to display. When omitted, all
        columns are displayed.

    height:
        Table height in pixels.

    hide_index:
        Whether the pandas index should be hidden.

    use_container_width:
        Whether the table should occupy the available page width.

    title:
        Optional table title.

    Notes
    -----
    The function does not modify the original DataFrame.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No data is available for this table."
        )

        return


    # ------------------------------------------------------------------------
    # Select columns
    # ------------------------------------------------------------------------

    table_df = dataframe.copy()

    if columns is not None:

        _validate_columns(
            table_df,
            columns,
        )

        table_df = table_df.loc[
            :,
            columns,
        ]


    # ------------------------------------------------------------------------
    # Optional title
    # ------------------------------------------------------------------------

    if title:

        st.markdown(
            f"**{title}**"
        )


    # ------------------------------------------------------------------------
    # Render table
    # ------------------------------------------------------------------------

    st.dataframe(
        table_df,
        use_container_width=use_container_width,
        height=height,
        hide_index=hide_index,
    )


# ============================================================================
# RANKED TABLE
# ============================================================================

def render_ranked_table(
    dataframe: pd.DataFrame,
    category_column: str,
    value_column: str,
    descending: bool = True,
    limit: int = 10,
    height: int = DEFAULT_RANKED_HEIGHT,
    title: Optional[str] = None,
) -> None:
    """
    Render a ranked analytical table.

    This component is intended for use cases such as:

    - Top customers by revenue
    - Highest-risk customers
    - Best-performing segments
    - Lowest-performing categories

    Parameters
    ----------
    dataframe:
        Source DataFrame.

    category_column:
        Column identifying the ranked entity.

    value_column:
        Numeric column used for ranking.

    descending:
        Whether larger values should appear first.

    limit:
        Maximum number of rows to display.

    height:
        Table height in pixels.

    title:
        Optional table title.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No ranking data is available."
        )

        return


    # ------------------------------------------------------------------------
    # Validate columns
    # ------------------------------------------------------------------------

    _validate_columns(
        dataframe,
        [
            category_column,
            value_column,
        ],
    )


    # ------------------------------------------------------------------------
    # Validate limit
    # ------------------------------------------------------------------------

    if limit <= 0:

        raise ValueError(
            "The ranking limit must be greater than zero."
        )


    # ------------------------------------------------------------------------
    # Build ranking
    # ------------------------------------------------------------------------

    ranked_df = (
        dataframe[
            [
                category_column,
                value_column,
            ]
        ]
        .copy()
        .sort_values(
            by=value_column,
            ascending=not descending,
        )
        .head(limit)
        .reset_index(drop=True)
    )


    # ------------------------------------------------------------------------
    # Add ranking position
    # ------------------------------------------------------------------------

    ranked_df.insert(
        0,
        "Rank",
        range(
            1,
            len(ranked_df) + 1,
        ),
    )


    # ------------------------------------------------------------------------
    # Optional title
    # ------------------------------------------------------------------------

    if title:

        st.markdown(
            f"**{title}**"
        )


    # ------------------------------------------------------------------------
    # Render ranking
    # ------------------------------------------------------------------------

    st.dataframe(
        ranked_df,
        use_container_width=True,
        height=height,
        hide_index=True,
    )


# ============================================================================
# COMPARISON TABLE
# ============================================================================

def render_comparison_table(
    dataframe: pd.DataFrame,
    label_column: str,
    metric_columns: list[str],
    height: int = DEFAULT_COMPARISON_HEIGHT,
    title: Optional[str] = None,
) -> None:
    """
    Render a structured comparison table.

    This is primarily intended for model-performance comparisons,
    but can also be used for comparing customer segments or
    business categories.

    Parameters
    ----------
    dataframe:
        Source comparison DataFrame.

    label_column:
        Column containing the entity/model name.

    metric_columns:
        Columns containing the metrics to compare.

    height:
        Table height in pixels.

    title:
        Optional table title.
    """

    if not _validate_dataframe(dataframe):

        _render_empty_state(
            "No comparison data is available."
        )

        return


    # ------------------------------------------------------------------------
    # Validate columns
    # ------------------------------------------------------------------------

    _validate_columns(
        dataframe,
        [
            label_column,
            *metric_columns,
        ],
    )


    # ------------------------------------------------------------------------
    # Select comparison columns
    # ------------------------------------------------------------------------

    comparison_df = dataframe[
        [
            label_column,
            *metric_columns,
        ]
    ].copy()


    # ------------------------------------------------------------------------
    # Optional title
    # ------------------------------------------------------------------------

    if title:

        st.markdown(
            f"**{title}**"
        )


    # ------------------------------------------------------------------------
    # Render comparison table
    # ------------------------------------------------------------------------

    st.dataframe(
        comparison_df,
        use_container_width=True,
        height=height,
        hide_index=True,
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "render_data_table",
    "render_ranked_table",
    "render_comparison_table",
]