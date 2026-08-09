"""
Reusable layout and container components.

This module provides the shared structural building blocks used by
dashboard pages.

Responsibilities
----------------
- Create consistent content panels.
- Provide reusable column layouts.
- Standardize spacing and grouping.
- Keep page layout code concise and consistent.

This module does not contain:
- business logic
- data loading
- metric calculations
- chart logic
- page-specific styling

Visual styling is controlled by the centralized dashboard theme.
"""

from __future__ import annotations

from contextlib import contextmanager
from html import escape
from typing import Iterator, Sequence

import streamlit as st


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_GAP = "medium"


# ============================================================================
# PANEL CONTAINER
# ============================================================================

@contextmanager
def panel(
    title: str | None = None,
    description: str | None = None,
    css_class: str = "dashboard-panel",
) -> Iterator[None]:
    """
    Create a reusable dashboard content panel.

    Parameters
    ----------
    title:
        Optional panel title.

    description:
        Optional supporting description.

    css_class:
        CSS class applied to the panel container.

    Example
    -------
    with panel(
        title="Revenue Performance",
        description="Monthly revenue trend."
    ):
        line_chart(...)
    """

    safe_css_class = escape(
        str(css_class)
    )

    header_html = ""

    if title:

        safe_title = escape(
            str(title)
        )

        description_html = ""

        if description:

            safe_description = escape(
                str(description)
            )

            description_html = (
                '<div class="dashboard-panel-description">'
                f"{safe_description}"
                "</div>"
            )

        header_html = (
            '<div class="dashboard-panel-header">'
            '<div class="dashboard-panel-title">'
            f"{safe_title}"
            "</div>"
            f"{description_html}"
            "</div>"
        )

    # Streamlit's container provides the actual content boundary.
    # The CSS class is attached through a lightweight wrapper so the
    # centralized theme can control the panel appearance.

    st.markdown(
        f'<div class="{safe_css_class}">',
        unsafe_allow_html=True,
    )

    if header_html:

        st.markdown(
            header_html,
            unsafe_allow_html=True,
        )

    try:

        yield

    finally:

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# ============================================================================
# SIMPLE CONTENT CONTAINER
# ============================================================================

@contextmanager
def content_container(
    css_class: str = "dashboard-content-container",
) -> Iterator[None]:
    """
    Create a generic content container.

    Useful when content needs a shared visual boundary but does not
    require a title or description.
    """

    safe_css_class = escape(
        str(css_class)
    )

    st.markdown(
        f'<div class="{safe_css_class}">',
        unsafe_allow_html=True,
    )

    try:

        yield

    finally:

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# ============================================================================
# TWO-COLUMN LAYOUT
# ============================================================================

def two_column_layout(
    ratio: Sequence[float] = (1.7, 1.0),
    gap: str = DEFAULT_GAP,
):
    """
    Create a reusable two-column layout.

    Parameters
    ----------
    ratio:
        Relative width of the two columns.

    gap:
        Streamlit column gap.

    Returns
    -------
    tuple
        Two Streamlit column containers.

    Example
    -------
    left, right = two_column_layout()

    with left:
        ...

    with right:
        ...
    """

    if len(ratio) != 2:

        raise ValueError(
            "two_column_layout requires exactly two column ratios."
        )

    if any(
        float(value) <= 0
        for value in ratio
    ):

        raise ValueError(
            "Column ratios must contain positive values."
        )

    return st.columns(
        list(ratio),
        gap=gap,
    )


# ============================================================================
# THREE-COLUMN LAYOUT
# ============================================================================

def three_column_layout(
    ratio: Sequence[float] = (1.0, 1.0, 1.0),
    gap: str = DEFAULT_GAP,
):
    """
    Create a reusable three-column layout.

    Returns
    -------
    tuple
        Three Streamlit column containers.
    """

    if len(ratio) != 3:

        raise ValueError(
            "three_column_layout requires exactly three column ratios."
        )

    if any(
        float(value) <= 0
        for value in ratio
    ):

        raise ValueError(
            "Column ratios must contain positive values."
        )

    return st.columns(
        list(ratio),
        gap=gap,
    )


# ============================================================================
# FOUR-COLUMN LAYOUT
# ============================================================================

def four_column_layout(
    ratio: Sequence[float] = (1.0, 1.0, 1.0, 1.0),
    gap: str = DEFAULT_GAP,
):
    """
    Create a reusable four-column layout.

    This is particularly useful for executive KPI rows.
    """

    if len(ratio) != 4:

        raise ValueError(
            "four_column_layout requires exactly four column ratios."
        )

    if any(
        float(value) <= 0
        for value in ratio
    ):

        raise ValueError(
            "Column ratios must contain positive values."
        )

    return st.columns(
        list(ratio),
        gap=gap,
    )


# ============================================================================
# RESPONSIVE COLUMN GROUP
# ============================================================================

def column_layout(
    columns: int,
    gap: str = DEFAULT_GAP,
):
    """
    Create a generic equal-width column layout.

    Parameters
    ----------
    columns:
        Number of columns.

    gap:
        Streamlit column gap.

    Returns
    -------
    list
        Streamlit column containers.
    """

    if columns < 1:

        raise ValueError(
            "The number of columns must be at least 1."
        )

    return st.columns(
        columns,
        gap=gap,
    )


# ============================================================================
# SPACER
# ============================================================================

def spacer(
    height: int = 16,
) -> None:
    """
    Add controlled vertical spacing.

    Parameters
    ----------
    height:
        Spacing height in pixels.

    Notes
    -----
    This uses a small HTML spacer rather than repeated blank
    Markdown statements, keeping page layout predictable.
    """

    if height < 0:

        raise ValueError(
            "Spacer height cannot be negative."
        )

    st.markdown(
        f'<div style="height:{int(height)}px;"></div>',
        unsafe_allow_html=True,
    )


# ============================================================================
# DIVIDER
# ============================================================================

def divider(
    spacing: str = "normal",
) -> None:
    """
    Render a consistent dashboard divider.

    Parameters
    ----------
    spacing:
        Semantic spacing class.

    Supported values
    ----------------
    compact
    normal
    spacious
    """

    spacing_classes = {
        "compact": "dashboard-divider-compact",
        "normal": "dashboard-divider",
        "spacious": "dashboard-divider-spacious",
    }

    if spacing not in spacing_classes:

        raise ValueError(
            f"Invalid divider spacing '{spacing}'. "
            f"Expected one of: {sorted(spacing_classes)}"
        )

    st.markdown(
        (
            f'<div class="{spacing_classes[spacing]}" '
            'aria-hidden="true"></div>'
        ),
        unsafe_allow_html=True,
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "panel",
    "content_container",
    "two_column_layout",
    "three_column_layout",
    "four_column_layout",
    "column_layout",
    "spacer",
    "divider",
]