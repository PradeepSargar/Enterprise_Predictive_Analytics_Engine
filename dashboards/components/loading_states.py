"""
Reusable loading-state components.

This module provides consistent loading feedback for the dashboard.

Supported components
--------------------
- loading_state()
- skeleton_card()
- skeleton_chart()
- loading_spinner()

Responsibilities
----------------
- Communicate that dashboard content is being prepared.
- Provide lightweight visual placeholders.
- Keep loading presentation consistent across pages.

This module does not:
- load data
- perform calculations
- manage application state
- contain business logic

All custom HTML is routed through the centralized HTML renderer.
"""

from __future__ import annotations

from contextlib import contextmanager
from html import escape
from typing import Iterator, Optional

import streamlit as st

from dashboards.utils.html import render_html


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_SKELETON_HEIGHT = 180


# ============================================================================
# LOADING STATE
# ============================================================================

def loading_state(
    message: str = "Loading dashboard data...",
    description: str = "",
) -> None:
    """
    Render a reusable loading-state message.

    Parameters
    ----------
    message:
        Primary loading message.

    description:
        Optional supporting explanation.
    """

    safe_message = escape(
        str(message)
    )

    safe_description = escape(
        str(description)
    )

    description_html = ""

    if description:

        description_html = (
            '<div class="loading-state-description">'
            f"{safe_description}"
            "</div>"
        )

    html = (
        '<div class="loading-state">'
        '<div class="loading-state-spinner" '
        'aria-hidden="true"></div>'
        '<div class="loading-state-message">'
        f"{safe_message}"
        "</div>"
        f"{description_html}"
        "</div>"
    )

    render_html(
        html
    )


# ============================================================================
# SKELETON CARD
# ============================================================================

def skeleton_card(
    label_width: str = "45%",
    value_width: str = "65%",
    footer_width: str = "35%",
) -> None:
    """
    Render a lightweight KPI/card skeleton.

    The skeleton provides visual structure while actual card content
    is being prepared.

    Parameters
    ----------
    label_width:
        Width of the simulated KPI label.

    value_width:
        Width of the simulated primary value.

    footer_width:
        Width of the simulated supporting text.
    """

    safe_label_width = escape(
        str(label_width)
    )

    safe_value_width = escape(
        str(value_width)
    )

    safe_footer_width = escape(
        str(footer_width)
    )

    html = (
        '<div class="skeleton-card">'
        '<div class="skeleton-line skeleton-label" '
        f'style="width:{safe_label_width};"></div>'
        '<div class="skeleton-line skeleton-value" '
        f'style="width:{safe_value_width};"></div>'
        '<div class="skeleton-line skeleton-footer" '
        f'style="width:{safe_footer_width};"></div>'
        "</div>"
    )

    render_html(
        html
    )


# ============================================================================
# SKELETON CHART
# ============================================================================

def skeleton_chart(
    height: int = DEFAULT_SKELETON_HEIGHT,
    title: Optional[str] = None,
) -> None:
    """
    Render a chart placeholder.

    Parameters
    ----------
    height:
        Approximate placeholder height in pixels.

    title:
        Optional chart title displayed above the placeholder.
    """

    if height <= 0:
        raise ValueError(
            "Skeleton chart height must be greater than zero."
        )

    title_html = ""

    if title:

        safe_title = escape(
            str(title)
        )

        title_html = (
            '<div class="skeleton-chart-title">'
            f"{safe_title}"
            "</div>"
        )

    html = (
        '<div class="skeleton-chart-wrapper">'
        f"{title_html}"
        '<div class="skeleton-chart" '
        f'style="height:{height}px;">'
        '<div class="skeleton-chart-grid"></div>'
        '<div class="skeleton-chart-line"></div>'
        "</div>"
        "</div>"
    )

    render_html(
        html
    )


# ============================================================================
# LOADING SPINNER
# ============================================================================

@contextmanager
def loading_spinner(
    message: str = "Loading...",
) -> Iterator[None]:
    """
    Provide a reusable Streamlit spinner context.

    Example
    -------
    with loading_spinner("Loading customer analytics..."):
        data = load_customer_data()

    Notes
    -----
    This uses Streamlit's native spinner rather than custom HTML.
    That keeps temporary processing feedback reliable and accessible.
    """

    with st.spinner(
        str(message)
    ):
        yield


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "loading_state",
    "skeleton_card",
    "skeleton_chart",
    "loading_spinner",
]