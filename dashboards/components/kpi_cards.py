"""
Reusable KPI card components.

This module provides the shared KPI card used throughout the
Enterprise Predictive Analytics Engine dashboard.

Design principles
-----------------
- One component = one KPI card.
- Pages provide data; this component only renders presentation.
- Business logic does not belong here.
- Styling is controlled by the centralized dashboard theme.
- The public ``kpi_card()`` API remains backward compatible.
- HTML content is escaped before rendering.
- Optional visual variants provide stronger dashboard hierarchy.
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

KPIAccent = Literal[
    "blue",
    "green",
    "purple",
    "amber",
    "red",
]


# ============================================================================
# CONSTANTS
# ============================================================================

SUPPORTED_DELTA_TYPES = {
    "positive",
    "negative",
    "neutral",
}

SUPPORTED_ACCENTS = {
    "blue",
    "green",
    "purple",
    "amber",
    "red",
}


# ============================================================================
# KPI CARD
# ============================================================================

def kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
    delta_type: DeltaType = "neutral",
    accent: KPIAccent = "blue",
    icon: str | None = None,
) -> None:
    """
    Render a reusable premium KPI card.

    Parameters
    ----------
    label:
        Short business name of the metric.

    value:
        Primary metric value displayed prominently.

    delta:
        Optional supporting information displayed below
        the primary value.

    delta_type:
        Semantic style for the supporting information.

        Supported values:
        - "positive"
        - "negative"
        - "neutral"

    accent:
        Visual accent applied to the top edge of the card.

        Supported values:
        - "blue"
        - "green"
        - "purple"
        - "amber"
        - "red"

    icon:
        Optional visual icon displayed inside the KPI card.

        Example:
            icon="◉"

        The icon is optional so existing pages using the
        original four-argument API continue to work.

    Notes
    -----
    The component does not inject CSS.

    All visual styling is provided by ``dashboards.styles.theme``.

    The component only creates the semantic HTML structure
    required by the centralized theme.
    """

    # ------------------------------------------------------------------------
    # Validate delta type
    # ------------------------------------------------------------------------

    if delta_type not in SUPPORTED_DELTA_TYPES:
        delta_type = "neutral"


    # ------------------------------------------------------------------------
    # Validate accent
    # ------------------------------------------------------------------------

    if accent not in SUPPORTED_ACCENTS:
        accent = "blue"


    # ------------------------------------------------------------------------
    # Normalize and escape dynamic values
    # ------------------------------------------------------------------------
    #
    # Values are converted to strings first so that callers can safely
    # provide numbers, pandas values, or other string-like objects.
    #
    # ``escape()`` prevents user/data content from becoming executable HTML.

    safe_label = escape(
        str(label)
    )

    safe_value = escape(
        str(value)
    )


    # ------------------------------------------------------------------------
    # Build optional icon
    # ------------------------------------------------------------------------

    icon_html = ""

    if icon is not None:

        safe_icon = escape(
            str(icon)
        )

        icon_html = (
            '<div class="kpi-icon">'
            f"{safe_icon}"
            "</div>"
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
    # ``kpi-{accent}`` allows the centralized theme to control the
    # visual accent without putting CSS directly into this component.
    #
    # Existing pages do not need to provide ``accent`` because blue
    # remains the safe default.

    html = (
        f'<div class="kpi-card kpi-{accent}">'

        '<div class="kpi-card-top">'

        '<div class="kpi-card-content">'

        '<div class="kpi-label">'
        f"{safe_label}"
        "</div>"

        '<div class="kpi-value">'
        f"{safe_value}"
        "</div>"

        f"{delta_html}"

        "</div>"

        f"{icon_html}"

        "</div>"

        "</div>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "kpi_card",
]