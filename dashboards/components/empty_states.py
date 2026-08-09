"""
Reusable empty-state components.

Empty states provide a consistent user experience when a dashboard
section has no data to display.

Typical cases
-------------
- No records match the selected filters.
- Forecast data is unavailable.
- Customer data is unavailable.
- A model result has not been generated.
- A dataset is empty.

This module contains presentation logic only.

Business logic, data loading, and filtering remain outside this
component.
"""

from __future__ import annotations

from html import escape
from typing import Literal

from dashboards.utils.html import render_html


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

EmptyStateType = Literal[
    "info",
    "warning",
    "error",
    "success",
]


# ============================================================================
# SUPPORTED TYPES
# ============================================================================

EMPTY_STATE_TYPES = {
    "info",
    "warning",
    "error",
    "success",
}


# ============================================================================
# CSS CLASS MAPPING
# ============================================================================

EMPTY_STATE_CLASS_MAP = {
    "info": "empty-state-info",
    "warning": "empty-state-warning",
    "error": "empty-state-error",
    "success": "empty-state-success",
}


# ============================================================================
# INTERNAL RENDERER
# ============================================================================

def _render_empty_state(
    title: str,
    description: str = "",
    state_type: EmptyStateType = "info",
    icon: str = "○",
) -> None:
    """
    Internal renderer shared by all empty-state variants.

    Parameters
    ----------
    title:
        Main empty-state message.

    description:
        Optional supporting explanation.

    state_type:
        Semantic visual state.

    icon:
        Small visual indicator displayed above the message.
    """

    # ------------------------------------------------------------------------
    # Validate state type
    # ------------------------------------------------------------------------

    if state_type not in EMPTY_STATE_TYPES:

        raise ValueError(
            f"Invalid state_type '{state_type}'. "
            f"Expected one of: {sorted(EMPTY_STATE_TYPES)}"
        )


    # ------------------------------------------------------------------------
    # Escape dynamic content
    # ------------------------------------------------------------------------

    safe_title = escape(
        str(title)
    )

    safe_description = escape(
        str(description)
    )

    safe_icon = escape(
        str(icon)
    )


    # ------------------------------------------------------------------------
    # Resolve semantic CSS class
    # ------------------------------------------------------------------------

    css_class = EMPTY_STATE_CLASS_MAP[
        state_type
    ]


    # ------------------------------------------------------------------------
    # Optional description
    # ------------------------------------------------------------------------

    description_html = ""

    if description:

        description_html = (
            '<div class="empty-state-description">'
            f"{safe_description}"
            "</div>"
        )


    # ------------------------------------------------------------------------
    # Build semantic HTML
    # ------------------------------------------------------------------------
    #
    # Keep markup compact and unindented.
    # The centralized renderer handles Streamlit HTML rendering.

    html = (
        f'<div class="empty-state {css_class}">'
        '<div class="empty-state-icon">'
        f"{safe_icon}"
        "</div>"
        '<div class="empty-state-title">'
        f"{safe_title}"
        "</div>"
        f"{description_html}"
        "</div>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    render_html(
        html
    )


# ============================================================================
# GENERIC EMPTY STATE
# ============================================================================

def empty_state(
    title: str = "No data available",
    description: str = "",
    state_type: EmptyStateType = "info",
    icon: str = "○",
) -> None:
    """
    Render a generic empty state.

    Parameters
    ----------
    title:
        Main message.

    description:
        Optional explanation.

    state_type:
        One of:
        - info
        - warning
        - error
        - success

    icon:
        Visual indicator displayed above the message.
    """

    _render_empty_state(
        title=title,
        description=description,
        state_type=state_type,
        icon=icon,
    )


# ============================================================================
# NO DATA STATE
# ============================================================================

def no_data_state(
    title: str = "No data available",
    description: str = (
        "There is currently no data available for this section."
    ),
) -> None:
    """
    Render a standard no-data message.
    """

    _render_empty_state(
        title=title,
        description=description,
        state_type="info",
        icon="○",
    )


# ============================================================================
# NO RESULTS STATE
# ============================================================================

def no_results_state(
    title: str = "No results found",
    description: str = (
        "No records match the current filters or selection."
    ),
) -> None:
    """
    Render a no-results message.

    This is intended for filtered dashboard views where the
    underlying dataset exists but the current selection produces
    zero records.
    """

    _render_empty_state(
        title=title,
        description=description,
        state_type="info",
        icon="⌕",
    )


# ============================================================================
# WARNING EMPTY STATE
# ============================================================================

def warning_empty_state(
    title: str = "Data requires attention",
    description: str = (
        "The requested data is currently unavailable or incomplete."
    ),
) -> None:
    """
    Render a warning empty state.
    """

    _render_empty_state(
        title=title,
        description=description,
        state_type="warning",
        icon="!",
    )


# ============================================================================
# ERROR EMPTY STATE
# ============================================================================

def error_empty_state(
    title: str = "Unable to display data",
    description: str = (
        "The requested dashboard data could not be displayed."
    ),
) -> None:
    """
    Render an error empty state.

    Use this for genuine data/display failures rather than ordinary
    situations where a filter simply returns zero records.
    """

    _render_empty_state(
        title=title,
        description=description,
        state_type="error",
        icon="×",
    )


# ============================================================================
# SUCCESS EMPTY STATE
# ============================================================================

def success_empty_state(
    title: str = "Nothing requires attention",
    description: str = (
        "There are currently no items requiring action."
    ),
) -> None:
    """
    Render a positive empty state.

    Useful for situations such as:
    - No high-risk customers
    - No pending alerts
    - No unresolved issues
    """

    _render_empty_state(
        title=title,
        description=description,
        state_type="success",
        icon="✓",
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "empty_state",
    "no_data_state",
    "no_results_state",
    "warning_empty_state",
    "error_empty_state",
    "success_empty_state",
]