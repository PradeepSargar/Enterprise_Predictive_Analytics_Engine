
"""
Reusable metric badge components.

Metric badges are compact semantic indicators used throughout the
dashboard to communicate status, direction, category, or risk level.

Examples
--------
HIGH RISK
LOW RISK
+19.4%
-7.2%
FORECAST
ACTUAL
ACTIVE
WARNING

Architecture
------------
Pages
    ↓
Metric badge component
    ↓
Centralized HTML renderer
    ↓
Global dashboard theme

This component contains presentation logic only.
Business calculations and metric interpretation remain outside
this module.
"""

from __future__ import annotations

from html import escape
from typing import Literal

from dashboards.utils.html import render_html


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

BadgeType = Literal[
    "positive",
    "negative",
    "neutral",
    "warning",
    "info",
]


# ============================================================================
# SUPPORTED BADGE TYPES
# ============================================================================

BADGE_TYPES = {
    "positive",
    "negative",
    "neutral",
    "warning",
    "info",
}


# ============================================================================
# CSS CLASS MAPPING
# ============================================================================

BADGE_CLASS_MAP = {
    "positive": "metric-badge-positive",
    "negative": "metric-badge-negative",
    "neutral": "metric-badge-neutral",
    "warning": "metric-badge-warning",
    "info": "metric-badge-info",
}


# ============================================================================
# INTERNAL RENDERER
# ============================================================================

def _render_badge(
    text: str,
    badge_type: BadgeType = "neutral",
) -> None:
    """
    Render a single metric badge.

    Parameters
    ----------
    text:
        Text displayed inside the badge.

    badge_type:
        Semantic type controlling the badge appearance.

    Raises
    ------
    ValueError
        If an unsupported badge type is provided.
    """

    # ------------------------------------------------------------------------
    # Validate badge type
    # ------------------------------------------------------------------------

    if badge_type not in BADGE_TYPES:

        raise ValueError(
            f"Invalid badge_type '{badge_type}'. "
            f"Expected one of: {sorted(BADGE_TYPES)}"
        )


    # ------------------------------------------------------------------------
    # Escape dynamic content
    # ------------------------------------------------------------------------
    #
    # Badge text may eventually come from model output or dataset values.
    # Escape it before placing it into HTML.

    safe_text = escape(
        str(text)
    )


    # ------------------------------------------------------------------------
    # Resolve semantic CSS class
    # ------------------------------------------------------------------------

    css_class = BADGE_CLASS_MAP[
        badge_type
    ]


    # ------------------------------------------------------------------------
    # Build HTML
    # ------------------------------------------------------------------------
    #
    # Keep the markup compact and unindented.
    # The centralized renderer handles Streamlit's HTML rendering.

    html = (
        f'<span class="metric-badge {css_class}">'
        f"{safe_text}"
        "</span>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    render_html(
        html
    )


# ============================================================================
# GENERIC METRIC BADGE
# ============================================================================

def metric_badge(
    text: str,
    badge_type: BadgeType = "neutral",
) -> None:
    """
    Render a generic metric badge.

    Parameters
    ----------
    text:
        Badge text.

    badge_type:
        Semantic badge state.

        Supported values:
        - positive
        - negative
        - neutral
        - warning
        - info

    Examples
    --------
    metric_badge(
        "HIGH VALUE",
        badge_type="positive",
    )

    metric_badge(
        "HIGH RISK",
        badge_type="negative",
    )
    """

    _render_badge(
        text=text,
        badge_type=badge_type,
    )


# ============================================================================
# POSITIVE BADGE
# ============================================================================

def positive_badge(
    text: str,
) -> None:
    """
    Render a positive metric badge.

    Use for favorable metrics, improvements, or healthy states.
    """

    _render_badge(
        text=text,
        badge_type="positive",
    )


# ============================================================================
# NEGATIVE BADGE
# ============================================================================

def negative_badge(
    text: str,
) -> None:
    """
    Render a negative metric badge.

    Use for unfavorable metrics, declines, or elevated risk.
    """

    _render_badge(
        text=text,
        badge_type="negative",
    )


# ============================================================================
# NEUTRAL BADGE
# ============================================================================

def neutral_badge(
    text: str,
) -> None:
    """
    Render a neutral metric badge.

    Use when the metric communicates information without
    implying positive or negative performance.
    """

    _render_badge(
        text=text,
        badge_type="neutral",
    )


# ============================================================================
# WARNING BADGE
# ============================================================================

def warning_badge(
    text: str,
) -> None:
    """
    Render a warning metric badge.

    Use for conditions that require attention but are not
    necessarily critical.
    """

    _render_badge(
        text=text,
        badge_type="warning",
    )


# ============================================================================
# INFO BADGE
# ============================================================================

def info_badge(
    text: str,
) -> None:
    """
    Render an informational metric badge.

    Use for contextual labels such as ACTUAL, FORECAST,
    or informational classifications.
    """

    _render_badge(
        text=text,
        badge_type="info",
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "metric_badge",
    "positive_badge",
    "negative_badge",
    "neutral_badge",
    "warning_badge",
    "info_badge",
]