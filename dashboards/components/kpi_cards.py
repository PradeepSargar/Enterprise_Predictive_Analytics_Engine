"""
Reusable KPI card components.

This module provides the shared KPI card used throughout the
Enterprise Predictive Analytics Engine dashboard.

Design principles
-----------------
- One component = one KPI card.
- Presentation styling remains controlled by the global theme.
- Pages provide data; this component only renders it.
- No business logic belongs here.
- No page-specific styling belongs here.
- The public API remains simple and reusable across all pages.
"""

from __future__ import annotations

from html import escape
from typing import Literal

import streamlit as st


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

DeltaType = Literal[
    "positive",
    "negative",
    "neutral",
]


# ============================================================================
# CONSTANTS
# ============================================================================

SUPPORTED_DELTA_TYPES = {
    "positive",
    "negative",
    "neutral",
}


# ============================================================================
# KPI CARD
# ============================================================================

def kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
    delta_type: DeltaType = "neutral",
) -> None:
    """
    Render a reusable premium KPI card.

    Parameters
    ----------
    label:
        Short name of the business metric.

    value:
        Primary metric value displayed prominently.

    delta:
        Optional supporting information displayed below the
        primary value.

    delta_type:
        Semantic styling for the supporting information.

        Supported values:
        - "positive"
        - "negative"
        - "neutral"

    Notes
    -----
    The component intentionally does not inject CSS.

    Visual styling is handled by the centralized dashboard
    theme so that every KPI card across every page remains
    visually consistent.
    """

    # ------------------------------------------------------------------------
    # Validate delta type
    # ------------------------------------------------------------------------
    #
    # Prevent accidental invalid CSS class names from being generated.
    # Falling back to "neutral" is safer than allowing arbitrary values
    # into the rendered HTML.

    if delta_type not in SUPPORTED_DELTA_TYPES:
        delta_type = "neutral"


    # ------------------------------------------------------------------------
    # Normalize values
    # ------------------------------------------------------------------------
    #
    # Convert values to strings before escaping them.
    # This allows callers to safely pass numbers or other string-like
    # values while keeping the public component API simple.

    safe_label = escape(
        str(label)
    )

    safe_value = escape(
        str(value)
    )


    # ------------------------------------------------------------------------
    # Build optional supporting information
    # ------------------------------------------------------------------------

    delta_html = ""

    if delta is not None:

        safe_delta = escape(
            str(delta)
        )

        delta_html = (
            '<div class="kpi-footer">'
            f'<span class="kpi-{delta_type}">'
            f"{safe_delta}"
            "</span>"
            "</div>"
        )


    # ------------------------------------------------------------------------
    # Build KPI card
    # ------------------------------------------------------------------------
    #
    # Keep the HTML as one continuous string.
    #
    # Streamlit's Markdown parser can interpret indented HTML as
    # code blocks. Building the markup without leading indentation
    # prevents the raw HTML from appearing visibly on the page.

    html = (
        '<div class="kpi-card">'
        '<div class="kpi-label">'
        f"{safe_label}"
        "</div>"
        '<div class="kpi-value">'
        f"{safe_value}"
        "</div>"
        f"{delta_html}"
        "</div>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    st.markdown(
        html,
        unsafe_allow_html=True,
    )