"""
Reusable dashboard header components.

This module provides the shared visual hierarchy used across
all dashboard pages.

Responsibilities
----------------
- Render the main page header.
- Render section headers.
- Render optional descriptions.
- Provide consistent semantic structure.
- Route all custom HTML through the centralized HTML renderer.

The component does not contain:
- business logic
- data loading
- page-specific styling
- CSS injection
"""

from __future__ import annotations

from html import escape

from dashboards.utils.html import render_html


# ============================================================================
# PAGE HEADER
# ============================================================================

def page_header(
    title: str,
    description: str = "",
    status: str = "LIVE ANALYTICS",
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

    Notes
    -----
    HTML is passed through the centralized ``render_html`` utility.
    This prevents individual components from implementing their own
    Streamlit HTML-rendering behavior.
    """

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
    # Header markup
    # ------------------------------------------------------------------------
    #
    # Keep the HTML compact and unindented.
    # The centralized renderer is responsible for safely passing the
    # markup to Streamlit.

    html = (
        '<div class="page-header">'
        '<div class="page-header-content">'
        '<div class="page-header-title">'
        f"{safe_title}"
        "</div>"
        f"{description_html}"
        "</div>"
        '<div class="page-header-status">'
        '<span class="status-badge status-live">'
        "● "
        f"{safe_status}"
        "</span>"
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
# SECTION HEADER
# ============================================================================

def section_header(
    title: str,
    description: str = "",
) -> None:
    """
    Render a section heading inside a dashboard page.

    Parameters
    ----------
    title:
        Section title.

    description:
        Optional explanation of the section's analytical purpose.
    """

    # ------------------------------------------------------------------------
    # Escape dynamic content
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
    # Section markup
    # ------------------------------------------------------------------------

    html = (
        '<div class="section-header">'
        '<div class="section-title">'
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
# SUBSECTION HEADER
# ============================================================================

def subsection_header(
    title: str,
    description: str = "",
) -> None:
    """
    Render a smaller analytical subsection heading.

    This is useful when a page contains multiple analytical blocks
    inside one major section.

    Parameters
    ----------
    title:
        Subsection title.

    description:
        Optional supporting description.
    """

    safe_title = escape(
        str(title)
    )

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


    html = (
        '<div class="subsection-header">'
        '<div class="subsection-title">'
        f"{safe_title}"
        "</div>"
        f"{description_html}"
        "</div>"
    )


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