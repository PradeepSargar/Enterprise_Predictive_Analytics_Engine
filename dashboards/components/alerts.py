"""
Reusable insight and alert components.

This module provides the shared semantic messaging components used
throughout the Enterprise Predictive Analytics Engine dashboard.

Supported semantic states
-------------------------
- danger
- warning
- success
- info

The components are intentionally presentation-focused.
Business logic remains in the data/transformation layer.

All custom HTML is routed through the centralized HTML renderer.
"""

from __future__ import annotations

from html import escape
from typing import Literal

from dashboards.utils.html import render_html


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

InsightType = Literal[
    "danger",
    "warning",
    "success",
    "info",
]


# ============================================================================
# SEMANTIC TYPES
# ============================================================================

INSIGHT_TYPES = {
    "danger": "danger",
    "warning": "warning",
    "success": "success",
    "info": "info",
}


# ============================================================================
# CSS CLASS MAPPING
# ============================================================================

INSIGHT_COLOR_CLASSES = {
    "danger": "insight-danger",
    "warning": "insight-warning",
    "success": "insight-success",
    "info": "insight-info",
}


# ============================================================================
# INTERNAL RENDERER
# ============================================================================

def _render_alert(
    label: str,
    title: str,
    description: str,
    insight_type: InsightType = "info",
) -> None:
    """
    Internal renderer shared by all alert and insight components.

    Keeping the HTML construction in one place prevents the four
    semantic alert variants from becoming duplicated implementations.
    """

    # ------------------------------------------------------------------------
    # Validate semantic type
    # ------------------------------------------------------------------------

    if insight_type not in INSIGHT_TYPES:

        raise ValueError(
            f"Invalid insight_type '{insight_type}'. "
            f"Expected one of: {sorted(INSIGHT_TYPES)}"
        )


    # ------------------------------------------------------------------------
    # Escape dynamic content
    # ------------------------------------------------------------------------
    #
    # Alert content normally comes from analytical results.
    # Escaping prevents metric values or generated text from being
    # interpreted as HTML.

    safe_label = escape(
        str(label)
    )

    safe_title = escape(
        str(title)
    )

    safe_description = escape(
        str(description)
    )


    # ------------------------------------------------------------------------
    # Resolve semantic CSS class
    # ------------------------------------------------------------------------

    color_class = INSIGHT_COLOR_CLASSES[
        insight_type
    ]


    # ------------------------------------------------------------------------
    # Build markup
    # ------------------------------------------------------------------------
    #
    # Keep the HTML compact and unindented.
    # The centralized renderer handles Streamlit HTML rendering.

    html = (
        '<div class="insight-card">'
        f'<div class="insight-label {color_class}">'
        f"{safe_label}"
        "</div>"
        '<div class="insight-title">'
        f"{safe_title}"
        "</div>"
        '<div class="insight-description">'
        f"{safe_description}"
        "</div>"
        "</div>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    render_html(
        html
    )


# ============================================================================
# GENERIC INSIGHT CARD
# ============================================================================

def insight_card(
    label: str,
    title: str,
    description: str,
    insight_type: InsightType = "info",
) -> None:
    """
    Render a business insight card.

    Parameters
    ----------
    label:
        Short category such as RETENTION, OPERATIONS, or FORECAST.

    title:
        Main insight statement.

    description:
        Supporting business explanation.

    insight_type:
        Semantic category controlling the visual state.

        Supported values:
        - "danger"
        - "warning"
        - "success"
        - "info"
    """

    _render_alert(
        label=label,
        title=title,
        description=description,
        insight_type=insight_type,
    )


# ============================================================================
# DANGER / RISK CARD
# ============================================================================

def risk_card(
    label: str,
    title: str,
    description: str,
) -> None:
    """
    Render a high-priority business risk insight.

    This is a convenience wrapper around ``insight_card()`` using
    the danger semantic state.
    """

    insight_card(
        label=label,
        title=title,
        description=description,
        insight_type="danger",
    )


# ============================================================================
# WARNING CARD
# ============================================================================

def warning_card(
    label: str,
    title: str,
    description: str,
) -> None:
    """
    Render a warning-level business insight.

    Use this for conditions requiring attention but not necessarily
    representing an immediate critical risk.
    """

    insight_card(
        label=label,
        title=title,
        description=description,
        insight_type="warning",
    )


# ============================================================================
# SUCCESS CARD
# ============================================================================

def success_card(
    label: str,
    title: str,
    description: str,
) -> None:
    """
    Render a positive business insight.

    Use this for favorable trends, successful model outcomes,
    or positive forecast signals.
    """

    insight_card(
        label=label,
        title=title,
        description=description,
        insight_type="success",
    )


# ============================================================================
# INFO CARD
# ============================================================================

def info_card(
    label: str,
    title: str,
    description: str,
) -> None:
    """
    Render a neutral informational insight.

    Use this when information is useful but should not be
    interpreted as positive or negative.
    """

    insight_card(
        label=label,
        title=title,
        description=description,
        insight_type="info",
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "insight_card",
    "risk_card",
    "warning_card",
    "success_card",
    "info_card",
]