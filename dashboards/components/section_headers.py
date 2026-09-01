"""
Reusable dashboard header components.

This module provides the shared visual hierarchy used across
all dashboard pages.

Responsibilities
----------------
- Render the main page header.
- Render section headers.
- Render subsection headers.
- Render optional descriptions.
- Provide consistent status styling.
- Escape dynamic content safely.
- Route all custom HTML through the centralized HTML renderer.

The component does not contain:
- business logic
- data loading
- page-specific styling
- CSS injection
"""

from __future__ import annotations

from html import escape
from typing import Literal

from dashboards.utils.html import render_html


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

HeaderStatus = Literal[
    "live",
    "warning",
    "danger",
    "info",
]


# ============================================================================
# CONSTANTS
# ============================================================================

SUPPORTED_STATUSES = {
    "live",
    "warning",
    "danger",
    "info",
}


# ============================================================================
# PAGE HEADER
# ============================================================================

def page_header(
    title: str,
    description: str = "",
    status: str = "LIVE ANALYTICS",
    status_type: HeaderStatus = "live",
) -> None:
    """
    Render the primary header for a dashboard page.

    Parameters
    ----------
    title:
        Main page title.

    description:
        Optional supporting description shown below the title.

    status:
        Status label displayed on the right side of the header.

    status_type:
        Visual status category.

        Supported values:
        - "live"
        - "warning"
        - "danger"
        - "info"

    Notes
    -----
    Dynamic content is escaped before being inserted into HTML.
    The HTML is rendered through the centralized ``render_html``
    utility so that Streamlit rendering remains consistent.
    """

    # ------------------------------------------------------------------------
    # Validate status type
    # ------------------------------------------------------------------------

    if status_type not in SUPPORTED_STATUSES:
        status_type = "live"


    # ------------------------------------------------------------------------
    # Escape dynamic content
    # ------------------------------------------------------------------------

    safe_title = escape(
        str(title)
    )

    safe_status = escape(
        str(status)
    )


    # ------------------------------------------------------------------------
    # Optional description
    # ------------------------------------------------------------------------

    description_html = ""

    if description:

        safe_description = escape(
            str(description)
        )

        description_html = (
            '<div class="page-header-description">'
            f"{safe_description}"
            "</div>"
        )


    # ------------------------------------------------------------------------
    # Status badge
    # ------------------------------------------------------------------------

    status_html = (
        '<div class="page-header-status">'

        f'<span class="status-badge status-{status_type}">'

        "● "

        f"{safe_status}"

        "</span>"

        "</div>"
    )


    # ------------------------------------------------------------------------
    # Build page header
    # ------------------------------------------------------------------------

    html = (
        '<div class="page-header">'

        '<div class="page-header-content">'

        '<div class="page-header-title">'
        f"{safe_title}"
        "</div>"

        f"{description_html}"

        "</div>"

        f"{status_html}"

        "</div>"
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    render_html(
        html
    )


# ============================================================================
# SECTION HEADER
# ============================================================================

def section_header(
    title: str,
    description: str = "",
) -> None:
    """
    Render a major analytical section heading.

    Parameters
    ----------
    title:
        Section title.

    description:
        Optional explanation of the section's analytical purpose.
    """

    # ------------------------------------------------------------------------
    # Escape title
    # ------------------------------------------------------------------------

    safe_title = escape(
        str(title)
    )


    # ------------------------------------------------------------------------
    # Optional description
    # ------------------------------------------------------------------------

    description_html = ""

    if description:

        safe_description = escape(
            str(description)
        )

        description_html = (
            '<div class="section-description">'
            f"{safe_description}"
            "</div>"
        )


    # ------------------------------------------------------------------------
    # Build section header with standout visual indicator & underline
    # ------------------------------------------------------------------------

    html = (
        '<div class="section-header">'
        '<div class="section-header-top">'
        '<div class="section-header-indicator"></div>'
        f'<div class="section-title">{safe_title}</div>'
        '</div>'
        f"{description_html}"
        '<div class="section-header-underline"></div>'
        '</div>'
    )


    # ------------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------------

    render_html(
        html
    )


# ============================================================================
# SUBSECTION HEADER
# ============================================================================

def subsection_header(
    title: str,
    description: str = "",
) -> None:
    """
    Render a smaller analytical subsection heading.

    Parameters
    ----------
    title:
        Subsection title.

    description:
        Optional supporting description.

    Notes
    -----
    Subsections intentionally use a lighter visual hierarchy than
    major section headers.
    """

    # ------------------------------------------------------------------------
    # Escape title
    # ------------------------------------------------------------------------

    safe_title = escape(
        str(title)
    )


    # ------------------------------------------------------------------------
    # Optional description
    # ------------------------------------------------------------------------

    description_html = ""

    if description:

        safe_description = escape(
            str(description)
        )

        description_html = (
            '<div class="subsection-description">'
            f"{safe_description}"
            "</div>"
        )


    # ------------------------------------------------------------------------
    # Build subsection header
    # ------------------------------------------------------------------------

    html = (
        '<div class="subsection-header">'

        '<div class="subsection-title">'
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
# PUBLIC API
# ============================================================================

__all__ = [
    "page_header",
    "section_header",
    "subsection_header",
]