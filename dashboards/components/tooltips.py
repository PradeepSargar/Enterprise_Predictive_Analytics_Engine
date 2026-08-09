"""
Reusable tooltip and contextual-help components.

This module provides lightweight contextual explanations for
dashboard metrics, controls, and analytical concepts.

The implementation intentionally uses Streamlit's native tooltip
support where possible instead of introducing custom JavaScript.

Responsibilities
----------------
- Provide reusable help text.
- Explain metrics and dashboard controls.
- Keep tooltip usage consistent across pages.
- Avoid custom JavaScript and fragile browser-specific behavior.

This module does not contain:
- business calculations
- data loading
- filtering logic
- page-specific business logic
"""

from __future__ import annotations

from typing import Optional

import streamlit as st


# ============================================================================
# BASIC TOOLTIP
# ============================================================================

def tooltip(
    text: str,
    icon: str = "ⓘ",
) -> None:
    """
    Render a small contextual-help tooltip.

    Parameters
    ----------
    text:
        Explanation displayed when the user hovers over the icon.

    icon:
        Character displayed as the tooltip trigger.

    Notes
    -----
    Streamlit's native tooltip support is used through the ``help``
    parameter. This avoids custom JavaScript and reduces rendering
    compatibility problems.
    """

    st.markdown(
        f'<span title="{text}">{icon}</span>',
        unsafe_allow_html=True,
    )


# ============================================================================
# HELP TEXT
# ============================================================================

def help_text(
    text: str,
    label: str = "ⓘ",
) -> None:
    """
    Render a compact contextual help indicator.

    This is useful beside section titles or analytical metrics.

    Parameters
    ----------
    text:
        Explanation shown when the user hovers over the indicator.

    label:
        Visible tooltip trigger.
    """

    tooltip(
        text=text,
        icon=label,
    )


# ============================================================================
# METRIC HELP
# ============================================================================

def metric_help(
    metric_name: str,
    explanation: str,
) -> None:
    """
    Render contextual help for a business metric.

    Example
    -------
    metric_help(
        "Average Order Value",
        "Total order-level revenue divided by total orders."
    )
    """

    tooltip_text = (
        f"{metric_name}: {explanation}"
    )

    tooltip(
        text=tooltip_text,
        icon="ⓘ",
    )


# ============================================================================
# FILTER HELP
# ============================================================================

def filter_help(
    explanation: str,
) -> None:
    """
    Render contextual help for a dashboard filter.
    """

    tooltip(
        text=explanation,
        icon="ⓘ",
    )


# ============================================================================
# CHART HELP
# ============================================================================

def chart_help(
    explanation: str,
) -> None:
    """
    Render contextual help for a chart.

    Useful for explaining:
    - forecast interpretation
    - confidence intervals
    - segment definitions
    - model metrics
    """

    tooltip(
        text=explanation,
        icon="ⓘ",
    )


# ============================================================================
# NATIVE STREAMLIT HELP
# ============================================================================

def help_label(
    label: str,
    help_text_value: Optional[str] = None,
) -> None:
    """
    Render a Streamlit-native label with optional help text.

    This helper is useful when building controls or sections where
    the help information should be associated directly with the label.

    Parameters
    ----------
    label:
        Visible label.

    help_text_value:
        Optional contextual explanation.
    """

    st.markdown(
        label,
        help=help_text_value,
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "tooltip",
    "help_text",
    "metric_help",
    "filter_help",
    "chart_help",
    "help_label",
]