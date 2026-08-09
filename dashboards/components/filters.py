"""
Reusable dashboard filter components.

This module provides the UI layer for dashboard filters.

Responsibilities
----------------
- Render reusable Streamlit filter controls.
- Provide consistent labels and defaults.
- Return the user's selected values.
- Keep filter UI separate from business logic and data transformations.

Architecture
------------
components/filters.py
    UI controls
          ↓
state/filters.py
    Stores shared filter selections
          ↓
data/transformation layer
    Applies business filtering
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, Optional

import pandas as pd
import streamlit as st


# ============================================================================
# DATE RANGE FILTER
# ============================================================================

def date_range_filter(
    label: str = "Date Range",
    min_date: Optional[date] = None,
    max_date: Optional[date] = None,
    default_start: Optional[date] = None,
    default_end: Optional[date] = None,
    key: Optional[str] = None,
) -> tuple[date, date]:
    """
    Render a reusable date-range filter.

    Returns
    -------
    tuple[date, date]
        Selected start and end dates.
    """

    today = date.today()

    if min_date is None:
        min_date = today

    if max_date is None:
        max_date = today

    if default_start is None:
        default_start = min_date

    if default_end is None:
        default_end = max_date

    selected_range = st.date_input(
        label,
        value=(default_start, default_end),
        min_value=min_date,
        max_value=max_date,
        key=key,
    )

    # Streamlit may return a single date when the widget is not
    # fully initialized as a range.
    if isinstance(selected_range, tuple):

        if len(selected_range) == 2:
            return selected_range[0], selected_range[1]

        if len(selected_range) == 1:
            return selected_range[0], selected_range[0]

    if isinstance(selected_range, list):

        if len(selected_range) >= 2:
            return selected_range[0], selected_range[1]

        if len(selected_range) == 1:
            return selected_range[0], selected_range[0]

    # Defensive fallback.
    return default_start, default_end


# ============================================================================
# SELECT FILTER
# ============================================================================

def select_filter(
    label: str,
    options: Iterable,
    default=None,
    key: Optional[str] = None,
    placeholder: Optional[str] = None,
):
    """
    Render a reusable single-select filter.

    Parameters
    ----------
    label:
        Filter label.

    options:
        Available choices.

    default:
        Optional default selection.

    key:
        Streamlit widget key.

    placeholder:
        Optional placeholder displayed by Streamlit.
    """

    options = list(options)

    if not options:
        st.info(
            f"No options available for {label}."
        )
        return None

    index = 0

    if default is not None and default in options:
        index = options.index(default)

    return st.selectbox(
        label,
        options=options,
        index=index,
        key=key,
        placeholder=placeholder,
    )


# ============================================================================
# MULTI-SELECT FILTER
# ============================================================================

def multiselect_filter(
    label: str,
    options: Iterable,
    default: Optional[Iterable] = None,
    key: Optional[str] = None,
) -> list:
    """
    Render a reusable multi-select filter.

    Returns
    -------
    list
        Selected options.
    """

    options = list(options)

    if not options:
        st.info(
            f"No options available for {label}."
        )
        return []

    if default is None:
        default_values = []
    else:
        default_values = [
            value
            for value in default
            if value in options
        ]

    return st.multiselect(
        label,
        options=options,
        default=default_values,
        key=key,
    )


# ============================================================================
# NUMBER RANGE FILTER
# ============================================================================

def number_range_filter(
    label: str,
    min_value: float,
    max_value: float,
    default_min: Optional[float] = None,
    default_max: Optional[float] = None,
    step: float = 1.0,
    key: Optional[str] = None,
) -> tuple[float, float]:
    """
    Render a reusable numeric range filter.

    Useful for:
    - Revenue
    - Customer value
    - Frequency
    - Recency
    - Risk probability
    """

    if default_min is None:
        default_min = min_value

    if default_max is None:
        default_max = max_value

    selected_range = st.slider(
        label,
        min_value=float(min_value),
        max_value=float(max_value),
        value=(
            float(default_min),
            float(default_max),
        ),
        step=float(step),
        key=key,
    )

    return selected_range[0], selected_range[1]


# ============================================================================
# CHECKBOX FILTER
# ============================================================================

def checkbox_filter(
    label: str,
    value: bool = False,
    key: Optional[str] = None,
) -> bool:
    """
    Render a reusable boolean filter.
    """

    return st.checkbox(
        label,
        value=value,
        key=key,
    )


# ============================================================================
# TOGGLE FILTER
# ============================================================================

def toggle_filter(
    label: str,
    value: bool = False,
    key: Optional[str] = None,
) -> bool:
    """
    Render a reusable toggle control.

    Useful for options such as:
    - Show high-risk customers only
    - Show forecast only
    - Show repeat customers only
    """

    return st.toggle(
        label,
        value=value,
        key=key,
    )


# ============================================================================
# FILTER RESET
# ============================================================================

def reset_filter_button(
    label: str = "Reset Filters",
    key: str = "reset_filters",
) -> bool:
    """
    Render a reusable filter-reset button.

    Returns
    -------
    bool
        True when the button is clicked.

    Notes
    -----
    This function intentionally does not manipulate session state
    directly. The state layer remains responsible for resetting
    stored filter values.
    """

    return st.button(
        label,
        key=key,
        use_container_width=True,
    )


# ============================================================================
# FILTER BAR
# ============================================================================

def filter_bar_start(
    title: Optional[str] = None,
) -> None:
    """
    Start a visual filter section.

    This function only provides lightweight structure.
    Global styling remains controlled by the dashboard theme.
    """

    if title:

        st.markdown(
            f"**{title}**"
        )


def filter_bar_end() -> None:
    """
    End a filter section.

    Kept as a dedicated function so the filter layout can later
    be enhanced centrally without changing individual pages.
    """

    st.divider()


# ============================================================================
# DATA-DRIVEN FILTER OPTIONS
# ============================================================================

def get_unique_options(
    dataframe: pd.DataFrame,
    column: str,
    include_all: bool = False,
    all_label: str = "All",
) -> list:
    """
    Return sorted unique values from a DataFrame column.

    Parameters
    ----------
    dataframe:
        Source DataFrame.

    column:
        Column from which options should be extracted.

    include_all:
        Whether to prepend an "All" option.

    all_label:
        Label used for the all-values option.
    """

    if dataframe is None:
        return []

    if column not in dataframe.columns:
        raise ValueError(
            f"Column '{column}' was not found in the DataFrame."
        )

    values = (
        dataframe[column]
        .dropna()
        .unique()
        .tolist()
    )

    try:
        values = sorted(values)
    except TypeError:
        # Some mixed-type columns cannot be directly sorted.
        values = sorted(
            values,
            key=lambda value: str(value),
        )

    if include_all:
        return [all_label, *values]

    return values


# ============================================================================
# DATA-DRIVEN SELECT FILTER
# ============================================================================

def dataframe_select_filter(
    dataframe: pd.DataFrame,
    column: str,
    label: Optional[str] = None,
    include_all: bool = True,
    all_label: str = "All",
    key: Optional[str] = None,
):
    """
    Create a select filter directly from a DataFrame column.

    This is a convenience function for dashboard pages.

    It does not filter the DataFrame itself.
    It only returns the user's selection.
    """

    if label is None:
        label = column.replace("_", " ").title()

    options = get_unique_options(
        dataframe=dataframe,
        column=column,
        include_all=include_all,
        all_label=all_label,
    )

    return select_filter(
        label=label,
        options=options,
        default=options[0] if options else None,
        key=key,
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "date_range_filter",
    "select_filter",
    "multiselect_filter",
    "number_range_filter",
    "checkbox_filter",
    "toggle_filter",
    "reset_filter_button",
    "filter_bar_start",
    "filter_bar_end",
    "get_unique_options",
    "dataframe_select_filter",
]