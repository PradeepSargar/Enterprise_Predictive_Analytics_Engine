"""
Reusable status indicator components.

Status indicators communicate the current state of a system,
business process, model, or dashboard element.

Examples
--------
LIVE
HEALTHY
WARNING
ERROR
PROCESSING

This component is presentation-only.

It does not:
- calculate status
- load data
- perform business logic
- manage application state

All custom HTML is routed through the centralized HTML renderer.
"""

from __future__ import annotations

from html import escape
from typing import Literal

from dashboards.utils.html import render_html


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

StatusType = Literal[
    "live",
    "healthy",
    "warning",
    "error",
    "processing",
    "inactive",
]


# ============================================================================
# SUPPORTED STATUS TYPES
# ============================================================================

STATUS_TYPES = {
    "live",
    "healthy",
    "warning",
    "error",
    "processing",
    "inactive",
}


# ============================================================================
# CSS CLASS MAPPING
# ============================================================================

STATUS_CLASS_MAP = {
    "live": "status-live",
    "healthy": "status-healthy",
    "warning": "status-warning",
    "error": "status-error",
    "processing": "status-processing",
    "inactive": "status-inactive",
}


# ============================================================================
# INTERNAL RENDERER
# ============================================================================

def _render_status(
    label: str,
    status_type: StatusType = "inactive",
    show_dot: bool = True,
) -> None:
    """
    Render a reusable status indicator.

    Parameters
    ----------
    label:
        Text displayed beside the status indicator.

    status_type:
        Semantic state controlling the visual styling.

    show_dot:
        Whether to display the status dot.
    """

    # ------------------------------------------------------------------------
    # Validate status type
    # ------------------------------------------------------------------------

    if status_type not in STATUS_TYPES:

        raise ValueError(
            f"Invalid status_type '{status_type}'. "
            f"Expected one of: {sorted(STATUS_TYPES)}"
        )


    # ------------------------------------------------------------------------
    # Escape dynamic content
    # ------------------------------------------------------------------------

    safe_label = escape(
        str(label)
    )


    # ------------------------------------------------------------------------
    # Resolve CSS class
    # ------------------------------------------------------------------------

    css_class = STATUS_CLASS_MAP[
        status_type
    ]


    # ------------------------------------------------------------------------
    # Optional status dot
    # ------------------------------------------------------------------------

    dot_html = ""

    if show_dot:

        dot_html = (
            '<span class="status-indicator-dot" '
            'aria-hidden="true"></span>'
        )


    # ------------------------------------------------------------------------
    # Build semantic status markup
    # ------------------------------------------------------------------------

    html = (
        f'<span class="status-indicator {css_class}" '
        f'aria-label="{safe_label}">'
        f"{dot_html}"
        '<span class="status-indicator-label">'
        f"{safe_label}"
        "</span>"
        "</span>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    render_html(
        html
    )


# ============================================================================
# GENERIC STATUS INDICATOR
# ============================================================================

def status_indicator(
    label: str,
    status_type: StatusType = "inactive",
    show_dot: bool = True,
) -> None:
    """
    Render a generic status indicator.

    Supported status types
    ----------------------
    live
    healthy
    warning
    error
    processing
    inactive
    """

    _render_status(
        label=label,
        status_type=status_type,
        show_dot=show_dot,
    )


# ============================================================================
# LIVE STATUS
# ============================================================================

def live_status(
    label: str = "LIVE",
) -> None:
    """
    Render a live/active status indicator.
    """

    _render_status(
        label=label,
        status_type="live",
    )


# ============================================================================
# HEALTHY STATUS
# ============================================================================

def healthy_status(
    label: str = "HEALTHY",
) -> None:
    """
    Render a healthy operational status indicator.
    """

    _render_status(
        label=label,
        status_type="healthy",
    )


# ============================================================================
# WARNING STATUS
# ============================================================================

def warning_status(
    label: str = "WARNING",
) -> None:
    """
    Render a warning status indicator.
    """

    _render_status(
        label=label,
        status_type="warning",
    )


# ============================================================================
# ERROR STATUS
# ============================================================================

def error_status(
    label: str = "ERROR",
) -> None:
    """
    Render an error status indicator.
    """

    _render_status(
        label=label,
        status_type="error",
    )


# ============================================================================
# PROCESSING STATUS
# ============================================================================

def processing_status(
    label: str = "PROCESSING",
) -> None:
    """
    Render a processing status indicator.
    """

    _render_status(
        label=label,
        status_type="processing",
    )


# ============================================================================
# INACTIVE STATUS
# ============================================================================

def inactive_status(
    label: str = "INACTIVE",
) -> None:
    """
    Render an inactive status indicator.
    """

    _render_status(
        label=label,
        status_type="inactive",
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "status_indicator",
    "live_status",
    "healthy_status",
    "warning_status",
    "error_status",
    "processing_status",
    "inactive_status",
]