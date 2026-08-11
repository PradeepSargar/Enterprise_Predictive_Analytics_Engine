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
    badge: str | None = None,
    footer_insight: str | None = None,
    css_class: str = "dashboard-panel",
) -> Iterator[None]:
    """
    Create a reusable dashboard content panel with glassmorphism styling.

    Parameters
    ----------
    title:
        Optional panel title.
    description:
        Optional supporting description.
    badge:
        Optional uppercase category/tag badge.
    footer_insight:
        Optional key analytical takeaway footer callout.
    css_class:
        CSS class applied to the panel container.
    """

    with st.container(border=True):

        if badge or title:

            safe_title = escape(str(title)) if title else ""
            safe_desc = escape(str(description)) if description else ""
            safe_badge = escape(str(badge)) if badge else ""

            badge_html = (
                f'<span class="dashboard-panel-badge">{safe_badge}</span>'
                if safe_badge
                else ""
            )

            title_html = (
                f'<div class="dashboard-panel-title">{safe_title}</div>'
                if safe_title
                else ""
            )

            desc_html = (
                f'<div class="dashboard-panel-description">{safe_desc}</div>'
                if safe_desc
                else ""
            )

            st.markdown(
                f"""
                <div class="dashboard-panel-header">
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.2rem;">
                        {title_html}
                        {badge_html}
                    </div>
                    {desc_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

        yield

        if footer_insight:

            safe_footer = escape(str(footer_insight))

            st.markdown(
                f"""
                <div class="dashboard-panel-footer">
                    <span class="dashboard-panel-footer-icon">💡</span>
                    <span class="dashboard-panel-footer-text">{safe_footer}</span>
                </div>
                """,
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