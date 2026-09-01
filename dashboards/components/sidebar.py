"""
Enterprise Predictive Analytics Engine - Sidebar Component
==========================================================

Modular, accessible executive sidebar component adhering to the
Forest Signal design system (#1B4332 primary, #F4A261 accent, #F1FAEE neutral).
Provides session state synchronization, keyboard accessibility,
and clean data-driven navigation grouping.
"""

from typing import Dict, List, Optional, Tuple
import streamlit as st

from dashboards.utils.html import render_html


# ---------------------------------------------------------------------------
# Data-Driven Navigation Configuration
# ---------------------------------------------------------------------------

SIDEBAR_SECTIONS: List[Tuple[str, List[Tuple[str, str, str]]]] = [
    (
        "Overview",
        [
            ("executive_overview", "Executive Overview", ":material/dashboard:"),
        ],
    ),
    (
        "Customer Intelligence",
        [
            ("customer_analytics", "Customer Analytics", ":material/groups:"),
            ("customer_risk", "Customer Risk", ":material/security:"),
            ("customer_segmentation", "Customer Segmentation", ":material/account_tree:"),
        ],
    ),
    (
        "Predictive Intelligence",
        [
            ("revenue_forecast", "Revenue Forecast", ":material/monitoring:"),
            ("model_performance", "Model Performance", ":material/model_training:"),
        ],
    ),
    (
        "Data & Insights",
        [
            ("data_explorer", "Data Explorer", ":material/table_view:"),
        ],
    ),
    (
        "System",
        [
            ("about", "About & Architecture", ":material/info:"),
        ],
    ),
]


def get_page_key(page_obj: st.Page, custom_keys: Optional[Dict[st.Page, str]] = None) -> str:
    """
    Retrieve a unique key for an st.Page instance safely.
    
    Uses explicit custom_keys mapping with a safe fallback to page title.
    Does not rely on private attributes.
    """
    if custom_keys and page_obj in custom_keys:
        return custom_keys[page_obj]
    
    title = getattr(page_obj, "title", "unknown")
    return str(title).lower().replace(" ", "_")


def render_sidebar_nav_link(
    page_obj: st.Page,
    label: str,
    icon: str,
    current_page: Optional[st.Page] = None,
    page_key_map: Optional[Dict[st.Page, str]] = None,
) -> None:
    """
    Render an accessible, high-contrast sidebar navigation link.
    
    Dynamically highlights the active page link with bold typography,
    accent indicators, and full CSS styling.
    """
    page_key = get_page_key(page_obj, page_key_map)
    active_key = st.session_state.get("active_page", "")
    is_active = (page_obj == current_page) if current_page is not None else (active_key == page_key)
    
    wrapper_class = (
        "sidebar-nav-item active sidebar-active-link-wrapper"
        if is_active
        else "sidebar-nav-item sidebar-link-wrapper"
    )
    aria_current = ' aria-current="page"' if is_active else ''
    data_active = ' data-nav-active="true"' if is_active else ' data-nav-active="false"'
    
    # Active items receive bold markdown label and helpful tooltip
    display_label = f"**{label}**" if is_active else label
    help_text = f"Currently Viewing: {label}" if is_active else f"Open {label}"
    
    render_html(f'<div class="{wrapper_class}"{aria_current}{data_active}>')
    st.page_link(
        page_obj,
        label=display_label,
        icon=icon,
        help=help_text,
    )
    render_html('</div>')


def render_sidebar(
    current_page: st.Page,
    pages: Dict[str, st.Page],
    brand_title: str = "ENTERPRISE",
    brand_subtitle: str = "Predictive Analytics Engine",
    status_text: str = "Engine Online • v2.4",
) -> None:
    """
    Render the complete enterprise sidebar navigation layout using a
    data-driven loop over SIDEBAR_SECTIONS.
    
    Parameters
    ----------
    current_page : st.Page
        The currently selected st.Page returned by st.navigation.
    pages : Dict[str, st.Page]
        Dictionary mapping page identifiers to st.Page instances.
    brand_title : str
        The primary brand header label.
    brand_subtitle : str
        The subtitle descriptor below the brand title.
    status_text : str
        Telemetry and status message in the sidebar footer.
    """
    # Build page keys mapping
    page_key_map = {page_obj: key for key, page_obj in pages.items()}
    
    # Synchronize session state with active page
    active_key = page_key_map.get(current_page, get_page_key(current_page, page_key_map))
    st.session_state["active_page"] = active_key

    # Resolve active page title for the prominent header card
    active_page_title = "Executive Overview"
    for section_label, nav_items in SIDEBAR_SECTIONS:
        for p_key, p_lbl, p_ico in nav_items:
            p_obj = pages.get(p_key) or pages.get(f"{p_key}_page")
            if p_obj and p_obj == current_page:
                active_page_title = p_lbl
                break

    with st.sidebar:
        # --------------------------------------------------------------------
        # Premium Executive Brand Header
        # --------------------------------------------------------------------
        render_html(
            '<div class="custom-sidebar-brand">'
            '<div class="sidebar-brand-mark" aria-hidden="true">◈</div>'
            '<div class="sidebar-brand-text">'
            '<div class="sidebar-brand-header-row">'
            f'<span class="sidebar-brand-title">{brand_title}</span>'
            '<span class="sidebar-brand-badge">AI / ML</span>'
            '</div>'
            f'<div class="sidebar-brand-subtitle">{brand_subtitle}</div>'
            '</div>'
            '</div>'
        )

        # Prominent Active Module Status Card
        render_html(
            '<div class="sidebar-current-view-card">'
            '<div class="sidebar-current-view-tag">'
            '<span class="sidebar-current-view-dot" aria-hidden="true"></span>'
            '<span>ACTIVE MODULE</span>'
            '</div>'
            f'<div class="sidebar-current-view-title">{active_page_title}</div>'
            '</div>'
        )

        # Divider
        render_html('<div class="sidebar-divider"></div>')

        # --------------------------------------------------------------------
        # Data-Driven Section Rendering Loop
        # --------------------------------------------------------------------
        for section_label, nav_items in SIDEBAR_SECTIONS:
            render_html(
                f'<div class="sidebar-section-label">'
                f'<span class="sidebar-section-indicator"></span>'
                f'<span>{section_label}</span>'
                f'</div>'
            )
            for page_key, label, icon in nav_items:
                page_obj = pages.get(page_key) or pages.get(f"{page_key}_page")
                if page_obj:
                    render_sidebar_nav_link(
                        page_obj=page_obj,
                        label=label,
                        icon=icon,
                        current_page=current_page,
                        page_key_map=page_key_map,
                    )

        # --------------------------------------------------------------------
        # Executive Telemetry Footer
        # --------------------------------------------------------------------
        render_html(
            '<div class="sidebar-footer">'
            '<div class="sidebar-footer-card">'
            '<div class="sidebar-footer-status">'
            '<span class="sidebar-status-dot" aria-hidden="true"></span>'
            f'<span class="sidebar-status-text">{status_text}</span>'
            '</div>'
            '<div class="sidebar-telemetry-meta">DuckDB OLAP • ML Engine Active</div>'
            '</div>'
            '</div>'
        )
