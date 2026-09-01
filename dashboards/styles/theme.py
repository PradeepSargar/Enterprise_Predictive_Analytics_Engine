"""
Enterprise Dashboard Design System (Decision-Intelligence Control Room)
========================================================================
Enterprise Predictive Analytics Engine

This module provides the centralized design system and global CSS injection for
the entire Streamlit analytics engine.

Design Direction:
- Premium enterprise decision-intelligence dashboard (predictive analytics,
  decision support, operational monitoring, forecasting, and risk awareness).
- High visual hierarchy, clean analytical canvas, solid cards with subtle shadows.
- Deep forest green executive sidebar navigation (#1B4332) with warm amber accents (#F4A261).
- Strict semantic color discipline (Forest Green=primary, Emerald=growth/positive,
  Amber=accent/alerts, Ocean=comparison, Crimson=risk/problem, Sage=neutral).
- Zero breaking changes to existing components, page links, or Streamlit APIs.
"""

from __future__ import annotations

import streamlit as st


# ============================================================================
# 1. COLOR SYSTEM DESIGN TOKENS (FOREST SIGNAL PALETTE)
# ============================================================================

COLORS = {
    # Application (Pale Mint-White Canvas & Pure White / Soft Mint Surfaces)
    "background": "#F1FAEE",
    "background_top": "#F1FAEE",
    "surface": "#FFFFFF",
    "surface_alt": "#E8F3E8",
    "surface_soft": "#DEEFE2",

    # Sidebar (Deep Forest Green Executive Panel)
    "sidebar": "#1B4332",
    "sidebar_surface": "#143628",
    "sidebar_hover": "#2D6A4F",
    "sidebar_active": "#F4A261",

    # Primary (Deep Forest Green — Headers, Nav)
    "primary": "#1B4332",
    "primary_dark": "#143628",
    "primary_light": "#D8F3DC",
    "primary_soft": "#E9F5ED",

    # Accent (Warm Amber — Alerts, CTAs, Positive Highlights)
    "accent": "#F4A261",
    "accent_dark": "#E76F51",
    "accent_light": "#FFE5D0",
    "accent_soft": "#FFF4EB",

    # Secondary (Growth Emerald Forest)
    "secondary": "#2D6A4F",
    "secondary_dark": "#1B4332",
    "secondary_light": "#D8F3DC",
    "secondary_soft": "#E8F5E9",

    # Success (Emerald Growth)
    "success": "#2D6A4F",
    "success_dark": "#1B4332",
    "success_light": "#D8F3DC",
    "success_soft": "#E8F5E9",

    # Warning (Warm Amber Attention & Highlights)
    "warning": "#F4A261",
    "warning_dark": "#E76F51",
    "warning_light": "#FFE5D0",
    "warning_soft": "#FFF4EB",

    # Danger (Coral Crimson Risk)
    "danger": "#E63946",
    "danger_dark": "#BA181B",
    "danger_light": "#FFE3E3",
    "danger_soft": "#FFF0F0",

    # Information (Steel Ocean Slate)
    "info": "#457B9D",
    "info_dark": "#1D3557",
    "info_light": "#D9E8F5",
    "info_soft": "#F0F6FA",

    # Text (Deep Forest Hierarchy)
    "text": "#112211",
    "text_secondary": "#2D4A3E",
    "text_muted": "#52796F",
    "text_light": "#84A98C",
    "text_inverse": "#FFFFFF",

    # Borders (Harmonious Mint-Slate Borders)
    "border": "#95BE9E",
    "border_light": "#C3DFC9",
    "border_strong": "#1B4332",

    # Miscellaneous
    "white": "#FFFFFF",
    "black": "#000000",
    "transparent": "rgba(0,0,0,0)",
}


# ============================================================================
# 2. CHART PALETTE (FOREST SIGNAL ANALYTICAL PALETTE)
# ============================================================================

CHART_PALETTE = [
    "#1B4332",  # Deep Forest Green (Primary Series)
    "#F4A261",  # Warm Amber (Accent / CTAs / Highlights)
    "#2D6A4F",  # Growth Emerald (Secondary Series)
    "#457B9D",  # Steel Ocean (Comparison Cohort)
    "#E63946",  # Coral Crimson (Risk / Friction)
    "#52796F",  # Muted Sage (Baseline / Benchmark)
]


# ============================================================================
# 3. TYPOGRAPHY
# ============================================================================

FONT_FAMILY = (
    "Inter, "
    "-apple-system, "
    "BlinkMacSystemFont, "
    '"Segoe UI", '
    "Roboto, "
    "Helvetica, "
    "Arial, "
    "sans-serif"
)


# ============================================================================
# 4. SHADOWS & RADIUS
# ============================================================================

SHADOWS = {
    "none": "none",
    "sm": "0 1px 3px rgba(15, 23, 42, 0.04)",
    "card": "0 2px 8px rgba(15, 23, 42, 0.05)",
    "hover": "0 6px 16px rgba(15, 23, 42, 0.08)",
}

RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "10px",
    "xl": "12px",
    "pill": "999px",
}

SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "0.75rem",
    "lg": "1rem",
    "xl": "1.5rem",
    "xxl": "2rem",
    "section": "2rem",
}


# ============================================================================
# 5. GLOBAL STYLE INJECTION
# ============================================================================

def inject_global_styles() -> None:
    """
    Inject the centralized enterprise decision-intelligence design system.
    Call this once from dashboards/app.py before rendering pages.
    """

    st.markdown(
        f"""
        <style>

        /* ==================================================================
           CSS VARIABLES (:ROOT DESIGN TOKENS)
           ================================================================== */

        :root {{
            --color-primary: {COLORS["primary"]};
            --color-primary-dark: {COLORS["primary_dark"]};
            --color-primary-light: {COLORS["primary_light"]};
            --color-primary-soft: {COLORS["primary_soft"]};
            --color-accent: {COLORS["accent"]};
            --color-accent-dark: {COLORS["accent_dark"]};
            --color-accent-light: {COLORS["accent_light"]};
            --color-accent-soft: {COLORS["accent_soft"]};
            --color-secondary: {COLORS["secondary"]};
            --color-secondary-dark: {COLORS["secondary_dark"]};
            --color-secondary-light: {COLORS["secondary_light"]};
            --color-secondary-soft: {COLORS["secondary_soft"]};
            --color-success: {COLORS["success"]};
            --color-success-dark: {COLORS["success_dark"]};
            --color-success-light: {COLORS["success_light"]};
            --color-success-soft: {COLORS["success_soft"]};
            --color-warning: {COLORS["warning"]};
            --color-warning-dark: {COLORS["warning_dark"]};
            --color-warning-light: {COLORS["warning_light"]};
            --color-warning-soft: {COLORS["warning_soft"]};
            --color-danger: {COLORS["danger"]};
            --color-danger-dark: {COLORS["danger_dark"]};
            --color-danger-light: {COLORS["danger_light"]};
            --color-danger-soft: {COLORS["danger_soft"]};
            --color-info: {COLORS["info"]};
            --color-info-dark: {COLORS["info_dark"]};
            --color-info-light: {COLORS["info_light"]};
            --color-info-soft: {COLORS["info_soft"]};
            
            --bg-canvas: {COLORS["background"]};
            --bg-canvas-top: {COLORS["background_top"]};
            --bg-surface: {COLORS["surface"]};
            --bg-surface-alt: {COLORS["surface_alt"]};
            --bg-surface-soft: {COLORS["surface_soft"]};
            
            --bg-sidebar: {COLORS["sidebar"]};
            --bg-sidebar-surface: {COLORS["sidebar_surface"]};
            --bg-sidebar-hover: {COLORS["sidebar_hover"]};
            --bg-sidebar-active: {COLORS["sidebar_active"]};
            --sidebar-width: 250px;
            
            --text-primary: {COLORS["text"]};
            --text-secondary: {COLORS["text_secondary"]};
            --text-muted: {COLORS["text_muted"]};
            --text-light: {COLORS["text_light"]};
            --text-inverse: {COLORS["text_inverse"]};
            
            --border-color: {COLORS["border"]};
            --border-light: {COLORS["border_light"]};
            --border-strong: {COLORS["border_strong"]};
            
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
            --radius-xl: 18px;
            --radius-pill: 9999px;
            
            --shadow-sm: 0 1px 2px 0 rgba(17, 34, 17, 0.05);
            --shadow-card: 0 1px 3px 0 rgba(17, 34, 17, 0.06), 0 1px 2px -1px rgba(17, 34, 17, 0.04);
            --shadow-hover: 0 10px 25px -5px rgba(17, 34, 17, 0.08), 0 8px 10px -6px rgba(17, 34, 17, 0.04);
            --shadow-glow: 0 0 20px -3px rgba(244, 162, 97, 0.35);
            --transition-smooth: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);

            /* Glide Data Grid & Streamlit Table Palette Variables */
            --gdg-accent-color: #1B4332;
            --gdg-accent-fg: #FFFFFF;
            --gdg-accent-light: rgba(27, 67, 50, 0.12);
            --gdg-text-dark: #112211;
            --gdg-text-medium: #2D4A3E;
            --gdg-text-light: #52796F;
            --gdg-text-bubble: #FFFFFF;
            --gdg-bg-icon-header: #D8F3DC;
            --gdg-fg-icon-header: #1B4332;
            --gdg-text-header: #F1FAEE;
            --gdg-text-header-selected: #FFFFFF;
            --gdg-bg-cell: #FFFFFF;
            --gdg-bg-cell-medium: #F8FCF9;
            --gdg-bg-header: #1B4332;
            --gdg-bg-header-has-focus: #143628;
            --gdg-bg-header-hovered: #2D6A4F;
            --gdg-bg-bubble: #1B4332;
            --gdg-bg-bubble-selected: #143628;
            --gdg-bg-search-result: #FFE5D0;
            --gdg-border-color: #C3DFC9;
            --gdg-drilldown-border: #95BE9E;
            --gdg-link-color: #1B4332;
            --gdg-cell-horizontal-padding: 12px;
            --gdg-cell-vertical-padding: 8px;
            --gdg-header-font-style: 700 12px {FONT_FAMILY};
            --gdg-base-font-style: 500 12.5px {FONT_FAMILY};

            --st-dataframe-header-background: #1B4332;
            --st-dataframe-header-color: #F1FAEE;
            --st-dataframe-border-color: #C3DFC9;
            --st-dataframe-cell-color: #112211;
            --st-dataframe-cell-background: #FFFFFF;
            --st-dataframe-cell-alternate-background: #F8FCF9;
            --st-dataframe-accent-color: #F4A261;
        }}


        /* ==================================================================
           GLOBAL SCROLLBAR & TYPOGRAPHY SMOOTHING
           ================================================================== */

        html, body, .stApp {{
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
            text-rendering: optimizeLegibility !important;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum" !important;
        }}

        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}

        ::-webkit-scrollbar-track {{
            background: transparent;
        }}

        ::-webkit-scrollbar-thumb {{
            background: rgba(148, 163, 184, 0.35);
            border-radius: 999px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--color-primary);
        }}


        /* ==================================================================
           ROOT APPLICATION CANVAS
           ================================================================== */

        .stApp,
        [data-testid="stAppViewContainer"] {{
            background-color: var(--bg-canvas) !important;
            color: var(--text-primary);
            font-family: {FONT_FAMILY};
        }}

        .main .block-container {{
            max-width: 1400px;
            padding-top: 1.25rem !important;
            padding-bottom: 3.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}


        /* ==================================================================
           TYPOGRAPHY & HIERARCHY
           ================================================================== */

        h1, h2, h3, h4, h5, h6 {{
            font-family: {FONT_FAMILY};
            color: var(--color-primary) !important;
            font-weight: 750;
            letter-spacing: -0.025em;
        }}

        h1 {{ font-size: 26px !important; line-height: 1.2 !important; }}
        h2 {{ font-size: 18px !important; line-height: 1.3 !important; }}
        h3 {{ font-size: 15px !important; font-weight: 650 !important; }}

        p, span, div {{
            font-family: {FONT_FAMILY};
        }}

        p {{
            font-size: 13px;
            line-height: 1.55;
            color: var(--text-secondary);
        }}


        /* ==================================================================
           FOREST EXECUTIVE SIDEBAR NAVIGATION (PREMIUM ELEVATED PANEL)
           ================================================================== */

        section[data-testid="stSidebar"],
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0F251C 0%, #153628 40%, #0C1E16 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.09) !important;
            box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.04), 4px 0 20px rgba(0, 0, 0, 0.16) !important;
            min-width: 275px !important;
            max-width: 320px !important;
            width: 285px !important;
        }}

        /* Subtle Dark Scrollbar for Sidebar */
        section[data-testid="stSidebar"] ::-webkit-scrollbar {{
            width: 5px !important;
        }}
        section[data-testid="stSidebar"] ::-webkit-scrollbar-track {{
            background: transparent !important;
        }}
        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.16) !important;
            border-radius: 4px !important;
        }}
        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.28) !important;
        }}

        section[data-testid="stSidebar"] > div:first-child {{
            background: transparent !important;
            padding-top: 0.75rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-bottom: 2rem !important;
            overflow-y: auto !important;
        }}

        section[data-testid="stSidebar"] * {{
            color: #E8ECEA !important;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 0.4rem 0 !important;
        }}

        /* Sidebar Navigation Items */
        .sidebar-nav-item,
        .sidebar-link-wrapper,
        [data-testid="stSidebar"] .stPageLink {{
            margin-bottom: 0.2rem !important;
            display: block !important;
        }}

        .sidebar-nav-item a,
        .sidebar-link-wrapper a,
        [data-testid="stSidebar"] .stPageLink a {{
            background: rgba(255, 255, 255, 0.035) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-left: 3px solid transparent !important;
            border-radius: 8px !important;
            padding: 0.48rem 0.75rem !important;
            font-size: 13.5px !important;
            font-weight: 500 !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.65rem !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            text-decoration: none !important;
            box-shadow: none !important;
        }}

        .sidebar-nav-item a span,
        .sidebar-nav-item a p,
        .sidebar-link-wrapper a span,
        .sidebar-link-wrapper a p,
        [data-testid="stSidebar"] .stPageLink a span,
        [data-testid="stSidebar"] .stPageLink a p {{
            color: #E2E8F0 !important;
            font-size: 13.5px !important;
            font-weight: 500 !important;
            letter-spacing: 0.01em !important;
            transition: color 0.2s ease !important;
        }}

        /* Tactile Floating Hover */
        .sidebar-nav-item:not(.active) a:hover,
        .sidebar-link-wrapper a:hover:not([aria-current="page"]):not([data-active="true"]),
        [data-testid="stSidebar"] .stPageLink a:hover:not([aria-current="page"]):not([data-active="true"]) {{
            background: rgba(255, 255, 255, 0.09) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-left: 3.5px solid rgba(244, 162, 97, 0.6) !important;
            transform: translateX(2px) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.22) !important;
        }}

        .sidebar-nav-item:not(.active) a:hover span,
        .sidebar-nav-item:not(.active) a:hover p,
        .sidebar-link-wrapper a:hover:not([aria-current="page"]):not([data-active="true"]) span,
        .sidebar-link-wrapper a:hover:not([aria-current="page"]):not([data-active="true"]) p,
        [data-testid="stSidebar"] .stPageLink a:hover:not([aria-current="page"]):not([data-active="true"]) span,
        [data-testid="stSidebar"] .stPageLink a:hover:not([aria-current="page"]):not([data-active="true"]) p {{
            color: #FFFFFF !important;
        }}

        /* Premium Active Navigation State (High Visual Distinction) */
        .sidebar-nav-item[data-nav-active="true"],
        .sidebar-nav-item.active,
        .sidebar-active-link-wrapper {{
            margin-bottom: 0.2rem !important;
            display: block !important;
        }}

        .sidebar-nav-item[data-nav-active="true"] a,
        .sidebar-nav-item.active a,
        .sidebar-active-link-wrapper a,
        [data-testid="stSidebar"] a:has(strong),
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] a:has(strong),
        [data-testid="stSidebar"] a[aria-current="page"],
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] a[aria-current="page"],
        [data-testid="stSidebar"] .stPageLink a[aria-current="page"],
        [data-testid="stSidebar"] .stPageLink a.active {{
            background: linear-gradient(90deg, rgba(244, 162, 97, 0.25) 0%, rgba(244, 162, 97, 0.06) 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(244, 162, 97, 0.45) !important;
            border-left: 4.5px solid #F4A261 !important;
            border-radius: 8px !important;
            padding: 0.48rem 0.75rem !important;
            font-weight: 700 !important;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.16) !important;
            transform: translateX(2px) !important;
        }}

        .sidebar-nav-item[data-nav-active="true"] a span,
        .sidebar-nav-item[data-nav-active="true"] a p,
        .sidebar-nav-item[data-nav-active="true"] a strong,
        .sidebar-nav-item.active a span,
        .sidebar-nav-item.active a p,
        .sidebar-nav-item.active a strong,
        .sidebar-active-link-wrapper a span,
        .sidebar-active-link-wrapper a p,
        .sidebar-active-link-wrapper a strong,
        [data-testid="stSidebar"] a:has(strong) span,
        [data-testid="stSidebar"] a:has(strong) p,
        [data-testid="stSidebar"] a:has(strong) strong,
        [data-testid="stSidebar"] a[aria-current="page"] span,
        [data-testid="stSidebar"] a[aria-current="page"] p,
        [data-testid="stSidebar"] a[aria-current="page"] strong,
        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] span,
        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] p,
        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] strong {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 13.5px !important;
            letter-spacing: 0.015em !important;
        }}

        .sidebar-nav-item[data-nav-active="true"] a [data-testid="stIconMaterial"],
        .sidebar-nav-item.active a [data-testid="stIconMaterial"],
        .sidebar-active-link-wrapper a [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] a:has(strong) [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] a[aria-current="page"] [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] [data-testid="stIconMaterial"] {{
            color: #F4A261 !important;
            font-size: 19px !important;
            filter: drop-shadow(0 0 8px rgba(244, 162, 97, 0.75)) !important;
            transform: scale(1.08) !important;
        }}

        /* Accessible Keyboard Focus States */
        .sidebar-nav-item a:focus-visible,
        .sidebar-link-wrapper a:focus-visible,
        [data-testid="stSidebar"] .stPageLink a:focus-visible {{
            outline: 2px solid #F4A261 !important;
            outline-offset: 2px !important;
        }}

        /* Sidebar Collapsed State (Icon-Only Mode Hook) */
        .sidebar-collapsed .sidebar-brand-text,
        .sidebar-collapsed .sidebar-section-label,
        .sidebar-collapsed .sidebar-footer-status > span:not(.sidebar-status-dot),
        .sidebar-collapsed .sidebar-nav-item a span,
        .sidebar-collapsed .sidebar-nav-item a p {{
            display: none !important;
        }}

        .sidebar-collapsed .sidebar-nav-item a {{
            justify-content: center !important;
            padding: 0.5rem 0 !important;
        }}

        .sidebar-collapsed .custom-sidebar-brand {{
            justify-content: center !important;
        }}


        /* ==================================================================
           SOLID CARDS & CONTENT PANELS (PREMIUM ELEVATION)
           ================================================================== */

        .dashboard-panel,
        .chart-card,
        .dashboard-content-container,
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: #FFFFFF !important;
            border: 2.5px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            padding: 1.25rem 1.35rem !important;
            margin-bottom: 1.25rem !important;
            box-shadow: 0 2px 8px 0 rgba(17, 34, 17, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            transition: var(--transition-smooth) !important;
            overflow: hidden !important;
            position: relative !important;
        }}

        .dashboard-panel:hover,
        .chart-card:hover,
        [data-testid="stVerticalBlockBorderWrapper"]:hover {{
            box-shadow: var(--shadow-hover) !important;
            border-color: var(--border-strong) !important;
            transform: translateY(-2px);
        }}

        .dashboard-panel-header,
        .chart-card-header {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            margin-bottom: 0.95rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border-light);
        }}

        .dashboard-panel-title,
        .chart-card-title {{
            font-size: 14.5px !important;
            font-weight: 750 !important;
            color: var(--color-primary) !important;
            letter-spacing: -0.015em;
            margin: 0;
        }}

        .dashboard-panel-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.22rem 0.55rem;
            border-radius: var(--radius-pill);
            font-size: 9.5px;
            font-weight: 750;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            background: var(--color-primary-soft);
            color: var(--color-primary);
            border: 2px solid var(--border-color);
        }}

        .dashboard-panel-description {{
            font-size: 12px;
            color: var(--text-muted);
            margin: 0;
            line-height: 1.45;
        }}

        .dashboard-panel-footer {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.95rem;
            border-top: 2px solid var(--border-light);
            background: var(--bg-surface-alt);
            margin-left: -1.35rem;
            margin-right: -1.35rem;
            margin-bottom: -1.25rem;
            padding: 0.75rem 1.35rem;
            font-size: 11.5px;
            color: var(--text-secondary);
        }}

        .dashboard-panel-footer-icon {{
            font-size: 14px;
        }}

        .dashboard-panel-footer-text {{
            font-size: 11.5px;
            font-weight: 550;
            color: var(--text-secondary);
        }}


        /* ==================================================================
           KPI CARDS (EXECUTIVE METRIC SCORECARDS)
           ================================================================== */

        .kpi-card,
        .metric-card {{
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
            border: 2.5px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            padding: 1.15rem 1.25rem !important;
            box-shadow: 0 2px 8px 0 rgba(17, 34, 17, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
            transition: var(--transition-smooth) !important;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 110px;
        }}

        .kpi-card:hover,
        .metric-card:hover {{
            box-shadow: var(--shadow-hover) !important;
            border-color: var(--border-strong) !important;
            transform: translateY(-2px);
        }}

        /* Subtle Accent Top Border Indicator */
        .kpi-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
        }}

        .kpi-card.kpi-blue::before {{ background: linear-gradient(90deg, #1B4332, #2D6A4F); }}
        .kpi-card.kpi-green::before {{ background: linear-gradient(90deg, #2D6A4F, #52B788); }}
        .kpi-card.kpi-purple::before {{ background: linear-gradient(90deg, #457B9D, #A8DADC); }}
        .kpi-card.kpi-amber::before {{ background: linear-gradient(90deg, #F4A261, #E76F51); }}
        .kpi-card.kpi-red::before {{ background: linear-gradient(90deg, #E63946, #F4A261); }}

        .kpi-card-top {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.5rem;
            width: 100%;
        }}

        .kpi-card-content {{
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
            width: 100%;
        }}

        .kpi-label {{
            font-size: 10.5px !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
            margin: 0 !important;
        }}

        .kpi-value {{
            font-size: 28px !important;
            font-weight: 800 !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.035em !important;
            line-height: 1.15 !important;
            margin: 0.2rem 0 !important;
            font-variant-numeric: tabular-nums !important;
        }}

        .kpi-footer {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            margin-top: 0.3rem;
        }}

        .kpi-positive {{
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
            font-size: 11.5px;
            font-weight: 650;
            color: var(--color-success);
        }}

        .kpi-negative {{
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
            font-size: 11.5px;
            font-weight: 650;
            color: var(--color-danger);
        }}

        .kpi-neutral {{
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
            font-size: 11.5px;
            font-weight: 550;
            color: var(--text-muted);
        }}

        .kpi-icon {{
            font-size: 14px;
            color: var(--text-muted);
            opacity: 0.7;
        }}


        /* ==================================================================
           DECISION INTELLIGENCE COMPONENT (.decision-card)
           ================================================================== */

        .decision-card {{
            background: var(--bg-surface);
            border: 2.5px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1.25rem 1.35rem;
            box-shadow: var(--shadow-card);
            margin-bottom: 1.15rem;
            position: relative;
        }}

        .decision-card-header {{
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }}

        .decision-verdict {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .decision-verdict.verdict-buy,
        .decision-verdict.verdict-book,
        .decision-verdict.verdict-low {{
            color: var(--color-success);
        }}

        .decision-verdict.verdict-wait,
        .decision-verdict.verdict-monitor,
        .decision-verdict.verdict-moderate {{
            color: var(--color-warning);
        }}

        .decision-verdict.verdict-avoid,
        .decision-verdict.verdict-high,
        .decision-verdict.verdict-critical {{
            color: var(--color-danger);
        }}

        .decision-metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.65rem 1rem;
            margin: 0.85rem 0;
            padding: 0.75rem 0;
            border-top: 2px solid var(--border-light);
            border-bottom: 2px solid var(--border-light);
        }}

        .decision-metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
        }}

        .decision-metric-label {{
            color: var(--text-muted);
        }}

        .decision-metric-val {{
            font-weight: 650;
            color: var(--text-primary);
            font-variant-numeric: tabular-nums;
        }}

        .decision-confidence-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: 0.25rem 0.6rem;
            border-radius: var(--radius-pill);
            background: var(--bg-surface-soft);
            color: var(--text-secondary);
            border: 2px solid var(--border-color);
        }}


        /* ==================================================================
           RISK VISUALIZATION HIERARCHY
           ================================================================== */

        .risk-badge-low {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.55rem;
            border-radius: var(--radius-pill);
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.04em;
            background: var(--color-success-soft);
            color: var(--color-success);
            border: 2px solid var(--color-success-light);
        }}

        .risk-badge-moderate {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.55rem;
            border-radius: var(--radius-pill);
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.04em;
            background: var(--color-warning-soft);
            color: var(--color-warning);
            border: 2px solid var(--color-warning-light);
        }}

        .risk-badge-high {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.55rem;
            border-radius: var(--radius-pill);
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.04em;
            background: var(--color-danger-soft);
            color: var(--color-danger);
            border: 2px solid var(--color-danger-light);
        }}

        .risk-badge-critical {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.55rem;
            border-radius: var(--radius-pill);
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.04em;
            background: #450A0A;
            color: #FEF2F2;
            border: 2px solid #991B1B;
        }}


        /* ==================================================================
           INSIGHT & ALERT CARDS
           ================================================================== */

        .insight-card {{
            background: var(--bg-surface);
            border: 2.5px solid var(--border-color);
            border-left: 6px solid var(--color-primary);
            border-radius: var(--radius-md);
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
        }}

        .insight-label {{
            font-size: 9.5px;
            font-weight: 750;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
            color: var(--color-primary);
        }}

        .insight-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }}

        .insight-description {{
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.45;
            margin: 0;
        }}

        .insight-card .insight-danger {{ color: var(--color-danger); }}
        .insight-card:has(.insight-danger) {{ border-left-color: var(--color-danger); background: var(--color-danger-soft); }}

        .insight-card .insight-warning {{ color: var(--color-warning); }}
        .insight-card:has(.insight-warning) {{ border-left-color: var(--color-warning); background: var(--color-warning-soft); }}

        .insight-card .insight-success {{ color: var(--color-success); }}
        .insight-card:has(.insight-success) {{ border-left-color: var(--color-success); background: var(--color-success-soft); }}

        .insight-card .insight-info {{ color: var(--color-info); }}
        .insight-card:has(.insight-info) {{ border-left-color: var(--color-info); background: var(--color-info-soft); }}


        /* ==================================================================
           STATUS INDICATORS
           ================================================================== */

        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.65rem;
            border-radius: var(--radius-pill);
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            background: var(--bg-surface);
            border: 1.5px solid var(--border-color);
        }}

        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
        }}

        .status-live .status-dot {{ background: var(--color-primary); }}
        .status-healthy .status-dot {{ background: var(--color-success); }}
        .status-warning .status-dot {{ background: var(--color-warning); }}
        .status-error .status-dot {{ background: var(--color-danger); }}
        .status-processing .status-dot {{ background: #7C3AED; }}
        .status-inactive .status-dot {{ background: var(--text-muted); }}


        /* ==================================================================
           STREAMLIT FORM CONTROLS, SELECTS, SLIDERS & BUTTONS
           ================================================================== */

        /* Buttons */
        .stButton > button {{
            background: var(--color-primary) !important;
            color: #FFFFFF !important;
            border: 2px solid var(--color-primary-dark) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.5rem 1.15rem !important;
            font-size: 12.5px !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition-smooth) !important;
        }}

        .stButton > button:hover {{
            background: var(--color-primary-dark) !important;
            box-shadow: var(--shadow-card) !important;
            transform: translateY(-1px);
        }}

        .stButton > button:active {{
            transform: translateY(0);
        }}

        .stDownloadButton > button {{
            background: var(--bg-surface) !important;
            color: var(--text-primary) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.45rem 0.95rem !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition-smooth) !important;
        }}

        .stDownloadButton > button:hover {{
            background: var(--bg-surface-alt) !important;
            border-color: var(--border-strong) !important;
            color: var(--color-primary) !important;
        }}

        /* Inputs & Selectboxes */
        div[data-baseweb="select"] > div {{
            background: var(--bg-surface) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-size: 12.5px !important;
        }}

        div[data-baseweb="select"] > div:hover {{
            border-color: var(--border-strong) !important;
        }}

        div[data-baseweb="select"] > div:focus-within {{
            border-color: var(--color-primary) !important;
            box-shadow: 0 0 0 2px var(--color-primary-light) !important;
        }}

        input[type="text"],
        input[type="number"],
        div[data-baseweb="input"] input {{
            background: var(--bg-surface) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            font-size: 12.5px !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1rem !important;
            background: transparent !important;
            border-bottom: 2px solid var(--border-color) !important;
            padding-bottom: 0 !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0.65rem 0.85rem !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            color: var(--text-muted) !important;
            border: none !important;
            background: transparent !important;
        }}

        .stTabs [aria-selected="true"] {{
            color: var(--color-primary) !important;
            border-bottom: 3px solid var(--color-primary) !important;
        }}


        /* ==================================================================
           DATA TABLES & DATAFRAMES (FOREST SIGNAL THEMED)
           ================================================================== */

        .stDataFrame,
        [data-testid="stDataFrame"],
        [data-testid="stDataFrameResizable"],
        [data-testid="stTable"],
        .dataframe {{
            --gdg-accent-color: #1B4332 !important;
            --gdg-accent-fg: #FFFFFF !important;
            --gdg-accent-light: rgba(27, 67, 50, 0.12) !important;
            --gdg-text-dark: #112211 !important;
            --gdg-text-medium: #2D4A3E !important;
            --gdg-text-light: #52796F !important;
            --gdg-text-bubble: #FFFFFF !important;
            --gdg-bg-icon-header: #D8F3DC !important;
            --gdg-fg-icon-header: #1B4332 !important;
            --gdg-text-header: #F1FAEE !important;
            --gdg-text-header-selected: #FFFFFF !important;
            --gdg-bg-cell: #FFFFFF !important;
            --gdg-bg-cell-medium: #F8FCF9 !important;
            --gdg-bg-header: #1B4332 !important;
            --gdg-bg-header-has-focus: #143628 !important;
            --gdg-bg-header-hovered: #2D6A4F !important;
            --gdg-bg-bubble: #1B4332 !important;
            --gdg-bg-bubble-selected: #143628 !important;
            --gdg-bg-search-result: #FFE5D0 !important;
            --gdg-border-color: #C3DFC9 !important;
            --gdg-drilldown-border: #95BE9E !important;
            --gdg-link-color: #1B4332 !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            overflow: hidden !important;
            background: #FFFFFF !important;
            box-shadow: 0 1px 3px 0 rgba(17, 34, 17, 0.05) !important;
        }}

        [data-testid="stDataFrame"] > div,
        [data-testid="stDataFrameResizable"] > div,
        [data-testid="stTable"] > div {{
            background: #FFFFFF !important;
        }}

        /* Streamlit Dataframe Canvas & Scroller */
        [data-testid="stDataFrame"] canvas,
        [data-testid="stDataFrameResizable"] canvas {{
            border-radius: calc(var(--radius-md) - 2px) !important;
        }}

        /* Dataframe Floating Action Toolbar */
        [data-testid="stDataFrameToolbar"],
        [data-testid="stDataFrame"] [data-testid="stElementToolbar"],
        [data-testid="stDataFrameResizable"] [data-testid="stElementToolbar"] {{
            background: #FFFFFF !important;
            border: 1.5px solid var(--border-color) !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(17, 34, 17, 0.08) !important;
            padding: 2px !important;
        }}

        [data-testid="stDataFrameToolbar"] button,
        [data-testid="stElementToolbar"] button {{
            color: var(--color-primary) !important;
            background: transparent !important;
            border: none !important;
            border-radius: 6px !important;
            transition: var(--transition-smooth) !important;
        }}

        [data-testid="stDataFrameToolbar"] button:hover,
        [data-testid="stElementToolbar"] button:hover {{
            background: var(--bg-surface-alt) !important;
            color: var(--color-primary-dark) !important;
        }}

        [data-testid="stDataFrameToolbar"] svg,
        [data-testid="stElementToolbar"] svg {{
            fill: var(--color-primary) !important;
            stroke: var(--color-primary) !important;
        }}

        /* Standard HTML Tables, Markdown Tables & Streamlit st.table */
        [data-testid="stTable"] table,
        table.dataframe,
        .stMarkdown table,
        div[data-testid="stMarkdownContainer"] table {{
            width: 100% !important;
            border-collapse: collapse !important;
            background: #FFFFFF !important;
            border-radius: var(--radius-md) !important;
            overflow: hidden !important;
            border: 1.5px solid var(--border-color) !important;
            margin: 0.5rem 0 !important;
        }}

        [data-testid="stTable"] th,
        .stDataFrame th,
        table.dataframe th,
        .dataframe th,
        .stMarkdown table th,
        div[data-testid="stMarkdownContainer"] table th,
        th.col_heading,
        th.row_heading,
        th.index_name {{
            background-color: #1B4332 !important;
            color: #F1FAEE !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
            padding: 0.65rem 0.85rem !important;
            border: none !important;
            border-bottom: 2px solid #143628 !important;
            text-align: left !important;
        }}

        [data-testid="stTable"] td,
        .stDataFrame td,
        table.dataframe td,
        .dataframe td,
        .stMarkdown table td,
        div[data-testid="stMarkdownContainer"] table td,
        td.data {{
            color: #112211 !important;
            font-size: 12.5px !important;
            padding: 0.6rem 0.85rem !important;
            border-bottom: 1px solid var(--border-light) !important;
            border-top: none !important;
            border-left: none !important;
            border-right: none !important;
            background-color: #FFFFFF !important;
        }}

        [data-testid="stTable"] tr:nth-child(even) td,
        table.dataframe tr:nth-child(even) td,
        .dataframe tr:nth-child(even) td,
        .stMarkdown table tr:nth-child(even) td,
        div[data-testid="stMarkdownContainer"] table tr:nth-child(even) td {{
            background-color: #F8FCF9 !important;
        }}

        [data-testid="stTable"] tr:hover td,
        table.dataframe tr:hover td,
        .dataframe tr:hover td,
        .stMarkdown table tr:hover td,
        div[data-testid="stMarkdownContainer"] table tr:hover td {{
            background-color: #E8F3E8 !important;
        }}

        /* Glide Data Grid Cells & Numbers */
        .stDataFrame [data-testid="glide-cell"] {{
            font-variant-numeric: tabular-nums !important;
            font-size: 12px !important;
            color: #112211 !important;
        }}

        /* Progress Bar & Highlight Accents */
        .stDataFrame [role="progressbar"],
        [data-testid="stDataFrame"] progress,
        [data-testid="stDataFrameResizable"] progress,
        progress {{
            accent-color: #F4A261 !important;
        }}

        progress::-webkit-progress-value {{
            background-color: #F4A261 !important;
            border-radius: 4px !important;
        }}

        progress::-webkit-progress-bar {{
            background-color: #DEEFE2 !important;
            border-radius: 4px !important;
        }}

        progress::-moz-progress-bar {{
            background-color: #F4A261 !important;
            border-radius: 4px !important;
        }}


        /* ==================================================================
           FINANCIAL SCENARIO PLANNING GUIDANCE CARD (EXECUTIVE MATRIX)
           ================================================================== */

        .scenario-planning-card {{
            background: #FFFFFF !important;
            border: 1.5px solid #C3DFC9 !important;
            border-radius: 10px !important;
            padding: 0.95rem 1rem !important;
            margin-top: 0.75rem !important;
            box-shadow: 0 2px 8px rgba(17, 34, 17, 0.05) !important;
        }}

        .scenario-planning-header {{
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 0.5rem !important;
            padding-bottom: 0.6rem !important;
            margin-bottom: 0.75rem !important;
            border-bottom: 1px solid #E8F3E8 !important;
        }}

        .scenario-planning-title {{
            display: flex !important;
            align-items: center !important;
            gap: 0.45rem !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            color: #1B4332 !important;
            letter-spacing: 0.02em !important;
        }}

        .scenario-header-icon {{
            font-size: 14px !important;
        }}

        .scenario-segment-pill {{
            background: #E8F5E9 !important;
            color: #1B4332 !important;
            border: 1px solid #C3DFC9 !important;
            border-radius: 4px !important;
            padding: 2px 8px !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: capitalize !important;
        }}

        .scenario-grid {{
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)) !important;
            gap: 0.65rem !important;
        }}

        .scenario-item {{
            border-radius: 8px !important;
            padding: 0.65rem 0.75rem !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 0.25rem !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }}

        .scenario-item:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06) !important;
        }}

        .scenario-bear {{
            background: #FFF5F5 !important;
            border: 1px solid #FFD6D6 !important;
        }}

        .scenario-base {{
            background: #F4FAF6 !important;
            border: 1.5px solid #A3D9B1 !important;
        }}

        .scenario-bull {{
            background: #F0F7FA !important;
            border: 1px solid #D0E4F0 !important;
        }}

        .scenario-label {{
            font-size: 10px !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
        }}

        .scenario-bear .scenario-label {{ color: #BA181B !important; }}
        .scenario-base .scenario-label {{ color: #1B4332 !important; }}
        .scenario-bull .scenario-label {{ color: #1D3557 !important; }}

        .scenario-value {{
            font-size: 15px !important;
            font-weight: 700 !important;
            font-feature-settings: "tnum" !important;
            line-height: 1.2 !important;
        }}

        .scenario-bear .scenario-value {{ color: #BA181B !important; }}
        .scenario-base .scenario-value {{ color: #1B4332 !important; }}
        .scenario-bull .scenario-value {{ color: #1D3557 !important; }}

        .scenario-badge {{
            display: inline-block !important;
            font-size: 10px !important;
            font-weight: 600 !important;
            border-radius: 4px !important;
            padding: 1px 6px !important;
            width: fit-content !important;
        }}

        .bear-badge {{
            background: #FFE3E3 !important;
            color: #BA181B !important;
        }}

        .base-badge {{
            background: #D8F3DC !important;
            color: #1B4332 !important;
        }}

        .bull-badge {{
            background: #D9E8F5 !important;
            color: #1D3557 !important;
        }}


        /* ==================================================================
           SIDEBAR BRAND & NAVIGATION CHROME (PREMIUM EXECUTIVE)
           ================================================================== */

        .custom-sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.7rem 0.8rem;
            margin-bottom: 0.35rem;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(0, 0, 0, 0.22) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
        }}

        .sidebar-brand-mark {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: linear-gradient(135deg, rgba(244, 162, 97, 0.25) 0%, rgba(45, 106, 79, 0.6) 100%);
            border: 1px solid rgba(244, 162, 97, 0.45);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #F4A261;
            font-size: 16px;
            font-weight: 600;
            flex-shrink: 0;
            box-shadow: 0 0 12px rgba(244, 162, 97, 0.25);
        }}

        .sidebar-brand-text {{
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            flex-grow: 1;
            min-width: 0;
        }}

        .sidebar-brand-header-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.4rem;
        }}

        .sidebar-brand-title {{
            font-size: 13.5px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            letter-spacing: 0.07em !important;
            line-height: 1.2;
            text-transform: uppercase;
        }}

        .sidebar-brand-badge {{
            font-size: 9px !important;
            font-weight: 700 !important;
            background: rgba(244, 162, 97, 0.15) !important;
            color: #F4A261 !important;
            border: 1px solid rgba(244, 162, 97, 0.35) !important;
            border-radius: 4px !important;
            padding: 1px 5px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            line-height: 1.2;
        }}

        .sidebar-brand-subtitle {{
            font-size: 10.5px !important;
            font-weight: 500 !important;
            color: #95BE9E !important;
            letter-spacing: 0.02em !important;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* Prominent Active Module Status Banner */
        .sidebar-current-view-card {{
            background: linear-gradient(135deg, rgba(244, 162, 97, 0.16) 0%, rgba(45, 106, 79, 0.32) 100%);
            border: 1px solid rgba(244, 162, 97, 0.38);
            border-radius: 8px;
            padding: 0.4rem 0.65rem;
            margin: 0.25rem 0 0.35rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}

        .sidebar-current-view-tag {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 9px !important;
            font-weight: 700 !important;
            color: #F4A261 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
        }}

        .sidebar-current-view-dot {{
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #52B788;
            box-shadow: 0 0 6px #52B788;
            animation: beaconPulse 2s infinite;
        }}

        .sidebar-current-view-title {{
            font-size: 12.5px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            letter-spacing: 0.02em !important;
            margin-top: 1px;
            line-height: 1.2;
        }}

        .sidebar-divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%);
            margin: 0.35rem 0.2rem;
        }}

        .sidebar-section-label {{
            display: flex !important;
            align-items: center !important;
            gap: 0.45rem !important;
            font-size: 10.5px !important;
            font-weight: 700 !important;
            color: #F4A261 !important;
            letter-spacing: 0.09em !important;
            text-transform: uppercase !important;
            padding: 0.55rem 0.45rem 0.2rem !important;
            margin: 0 !important;
        }}

        .sidebar-section-indicator {{
            display: inline-block;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: #F4A261;
            box-shadow: 0 0 4px rgba(244, 162, 97, 0.6);
            opacity: 0.95;
            flex-shrink: 0;
        }}

        /* Executive Telemetry Status Footer (Relative Flow - Never Blocks Page Links) */
        .sidebar-footer {{
            position: relative !important;
            width: 100% !important;
            margin-top: 0.85rem !important;
            margin-bottom: 0.35rem !important;
            padding: 0 !important;
            background: transparent !important;
            border: none !important;
            z-index: 10 !important;
        }}

        .sidebar-footer-card {{
            background: rgba(0, 0, 0, 0.28) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            padding: 0.45rem 0.6rem !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 0.15rem !important;
        }}

        .sidebar-footer-status {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }}

        .sidebar-status-text {{
            font-size: 11px !important;
            font-weight: 600 !important;
            color: #FFFFFF !important;
            letter-spacing: 0.02em;
        }}

        .sidebar-telemetry-meta {{
            font-size: 9.5px !important;
            font-weight: 500 !important;
            color: #7EA28B !important;
            letter-spacing: 0.03em;
            padding-left: 0.95rem;
        }}

        @keyframes beaconPulse {{
            0% {{
                box-shadow: 0 0 0 0 rgba(82, 183, 136, 0.8);
            }}
            70% {{
                box-shadow: 0 0 0 6px rgba(82, 183, 136, 0);
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(82, 183, 136, 0);
            }}
        }}

        .sidebar-status-dot {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #52B788;
            animation: beaconPulse 2.2s infinite;
            flex-shrink: 0;
        }}

        /* Respect accessibility preferences for reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}


        /* ==================================================================
           GLOBAL APPLICATION HEADER BAR
           ================================================================== */

        .app-global-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.85rem 1.35rem;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.02), inset 0 1px 0 rgba(255, 255, 255, 0.9);
            margin-bottom: 1.35rem;
            flex-wrap: wrap;
        }}

        .badge-micro-label {{
            font-size: 9.5px;
            font-weight: 750;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            line-height: 1.3;
        }}

        .badge-micro-value {{
            font-size: 13px;
            font-weight: 750;
            color: var(--text-primary);
            letter-spacing: -0.015em;
        }}


        /* ==================================================================
           PAGE HEADER COMPONENT
           ================================================================== */

        .page-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1.25rem;
            padding-bottom: 1.15rem;
            margin-bottom: 1.35rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .page-header-content {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            flex: 1;
        }}

        .page-header-title {{
            font-size: 26px !important;
            font-weight: 850 !important;
            color: var(--color-primary) !important;
            letter-spacing: -0.03em;
            margin: 0;
            line-height: 1.2;
        }}

        .page-header-description {{
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.55;
            margin: 0;
            max-width: 750px;
        }}

        .page-header-status {{
            flex-shrink: 0;
        }}

        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.85rem;
            border-radius: var(--radius-pill);
            font-size: 10px;
            font-weight: 750;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            white-space: nowrap;
        }}

        .status-badge.status-live {{
            color: var(--color-primary);
            border-color: rgba(37, 99, 235, 0.25);
            background: var(--color-primary-soft);
        }}

        .status-badge.status-warning {{
            color: var(--color-warning);
            border-color: rgba(245, 158, 11, 0.25);
            background: var(--color-warning-soft);
        }}

        .status-badge.status-danger {{
            color: var(--color-danger);
            border-color: rgba(244, 63, 94, 0.25);
            background: var(--color-danger-soft);
        }}

        .status-badge.status-info {{
            color: var(--color-info);
            border-color: rgba(99, 102, 241, 0.25);
            background: var(--color-info-soft);
        }}


        /* ==================================================================
           SECTION & SUBSECTION HEADERS
           ================================================================== */

        .section-header {{
            margin-top: 2.25rem;
            margin-bottom: 1.15rem;
            position: relative;
        }}

        .section-header-top {{
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.35rem;
        }}

        .section-header-indicator {{
            width: 5px;
            height: 20px;
            border-radius: 4px;
            background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-accent) 100%);
            box-shadow: 0 0 10px rgba(244, 162, 97, 0.45);
            flex-shrink: 0;
        }}

        .section-title {{
            font-size: 17.5px !important;
            font-weight: 850 !important;
            color: var(--color-primary) !important;
            letter-spacing: -0.02em;
            margin: 0;
            line-height: 1.25;
        }}

        .section-description {{
            font-size: 12.5px;
            color: var(--text-muted);
            margin: 0 0 0.65rem 0.9rem;
            line-height: 1.5;
            max-width: 820px;
        }}

        .section-header-underline {{
            height: 3px;
            border-radius: 2px;
            background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-accent) 80px, rgba(149, 190, 158, 0.8) 80px, rgba(149, 190, 158, 0.8) 100%);
            width: 100%;
        }}

        .subsection-header {{
            margin-top: 1.35rem;
            margin-bottom: 0.75rem;
            padding-left: 0.5rem;
            border-left: 3px solid var(--color-primary-light);
        }}

        .subsection-title {{
            font-size: 14.5px !important;
            font-weight: 750 !important;
            color: var(--color-primary) !important;
            letter-spacing: -0.01em;
            margin: 0;
        }}

        .subsection-description {{
            font-size: 12px;
            color: var(--text-muted);
            margin: 0.15rem 0 0 0;
            line-height: 1.45;
        }}


        /* ==================================================================
           DASHBOARD DIVIDERS
           ================================================================== */

        .dashboard-divider {{
            height: 2px;
            background: var(--border-color);
            margin: 1.25rem 0;
        }}

        .dashboard-divider-compact {{
            height: 2px;
            background: var(--border-color);
            margin: 0.65rem 0;
        }}

        .dashboard-divider-spacious {{
            height: 2px;
            background: var(--border-color);
            margin: 2rem 0;
        }}


        /* ==================================================================
           LOADING STATES & SKELETON SCREENS
           ================================================================== */

        .loading-state {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem 1.5rem;
            gap: 1rem;
            text-align: center;
        }}

        .loading-state-spinner {{
            width: 36px;
            height: 36px;
            border: 3px solid var(--border-light);
            border-top-color: var(--color-primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .loading-state-message {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .loading-state-description {{
            font-size: 12px;
            color: var(--text-muted);
            max-width: 320px;
        }}

        .skeleton-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
        }}

        .skeleton-line {{
            background: linear-gradient(90deg, var(--bg-surface-soft) 25%, var(--bg-surface-alt) 50%, var(--bg-surface-soft) 75%);
            background-size: 200% 100%;
            animation: skeleton-shimmer 1.5s ease-in-out infinite;
            border-radius: var(--radius-sm);
        }}

        @keyframes skeleton-shimmer {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}

        .skeleton-label {{
            width: 45%;
            height: 10px;
        }}

        .skeleton-value {{
            width: 65%;
            height: 22px;
        }}

        .skeleton-footer {{
            width: 55%;
            height: 9px;
        }}

        .skeleton-chart-wrapper {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1.25rem;
        }}

        .skeleton-chart-title {{
            width: 40%;
            height: 14px;
            background: var(--bg-surface-soft);
            border-radius: var(--radius-sm);
            margin-bottom: 1rem;
        }}

        .skeleton-chart {{
            height: 200px;
            position: relative;
            overflow: hidden;
        }}

        .skeleton-chart-grid {{
            position: absolute;
            inset: 0;
            background-image:
                linear-gradient(to right, var(--border-light) 1px, transparent 1px),
                linear-gradient(to bottom, var(--border-light) 1px, transparent 1px);
            background-size: 20% 25%;
        }}

        .skeleton-chart-line {{
            position: absolute;
            bottom: 30%;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--bg-surface-soft);
            border-radius: 1px;
        }}


        /* ==================================================================
           EMPTY STATES
           ================================================================== */

        .empty-state {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 3rem 2rem;
            gap: 0.65rem;
            background: var(--bg-surface);
            border: 1px dashed var(--border-color);
            border-radius: var(--radius-md);
        }}

        .empty-state-icon {{
            font-size: 32px;
            opacity: 0.6;
        }}

        .empty-state-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .empty-state-description {{
            font-size: 12px;
            color: var(--text-muted);
            max-width: 360px;
            line-height: 1.45;
        }}

        .empty-state-info {{ border-color: var(--color-info); }}
        .empty-state-info .empty-state-icon {{ color: var(--color-info); }}

        .empty-state-warning {{ border-color: var(--color-warning); }}
        .empty-state-warning .empty-state-icon {{ color: var(--color-warning); }}

        .empty-state-error {{ border-color: var(--color-danger); }}
        .empty-state-error .empty-state-icon {{ color: var(--color-danger); }}

        .empty-state-success {{ border-color: var(--color-success); }}
        .empty-state-success .empty-state-icon {{ color: var(--color-success); }}


        /* ==================================================================
           METRIC BADGES
           ================================================================== */

        .metric-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.2rem 0.55rem;
            border-radius: var(--radius-pill);
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 0.03em;
            background: var(--bg-surface);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }}

        .metric-badge-positive {{
            background: var(--color-success-soft);
            color: var(--color-success);
            border-color: var(--color-success-light);
        }}

        .metric-badge-negative {{
            background: var(--color-danger-soft);
            color: var(--color-danger);
            border-color: var(--color-danger-light);
        }}

        .metric-badge-neutral {{
            background: var(--bg-surface-soft);
            color: var(--text-muted);
            border-color: var(--border-color);
        }}

        .metric-badge-warning {{
            background: var(--color-warning-soft);
            color: var(--color-warning);
            border-color: var(--color-warning-light);
        }}

        .metric-badge-info {{
            background: var(--color-info-soft);
            color: var(--color-info);
            border-color: var(--color-info-light);
        }}


        /* ==================================================================
           STATUS INDICATOR SUBCLASSES
           ================================================================== */

        .status-indicator-dot {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        .status-indicator-label {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .status-live .status-indicator-dot {{ background: var(--color-primary); box-shadow: 0 0 6px var(--color-primary); }}
        .status-healthy .status-indicator-dot {{ background: var(--color-success); box-shadow: 0 0 6px var(--color-success); }}
        .status-warning .status-indicator-dot {{ background: var(--color-warning); box-shadow: 0 0 6px var(--color-warning); }}
        .status-error .status-indicator-dot {{ background: var(--color-danger); box-shadow: 0 0 6px var(--color-danger); }}
        .status-processing .status-indicator-dot {{ background: #7C3AED; box-shadow: 0 0 6px #7C3AED; }}
        .status-inactive .status-indicator-dot {{ background: var(--text-light); }}


        /* ==================================================================
           STREAMLIT EXPANDER POLISH
           ================================================================== */

        .streamlit-expanderHeader {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            border-radius: var(--radius-md) !important;
            background: var(--bg-surface) !important;
            border: 2px solid var(--border-color) !important;
        }}

        details[data-testid="stExpander"] {{
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            background: var(--bg-surface) !important;
            box-shadow: var(--shadow-sm) !important;
        }}

        details[data-testid="stExpander"] summary {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }}


        /* ==================================================================
           STREAMLIT MULTISELECT TAGS
           ================================================================== */

        span[data-baseweb="tag"] {{
            background: var(--color-primary-soft) !important;
            color: var(--color-primary) !important;
            border: 1.5px solid var(--color-primary-light) !important;
            border-radius: var(--radius-sm) !important;
            font-size: 11px !important;
            font-weight: 600 !important;
        }}


        /* ==================================================================
           STREAMLIT METRIC OVERRIDE
           ================================================================== */

        [data-testid="stMetric"] {{
            background: var(--bg-surface) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.85rem 1rem !important;
            box-shadow: var(--shadow-card) !important;
        }}

        [data-testid="stMetric"] label {{
            font-size: 10px !important;
            font-weight: 650 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
        }}

        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 22px !important;
            font-weight: 750 !important;
            color: var(--text-primary) !important;
            font-variant-numeric: tabular-nums !important;
        }}


        /* ==================================================================
           STREAMLIT TABS (LUXURY FINTECH STYLE)
           ================================================================== */

        [data-testid="stTabs"] [data-baseweb="tab-list"] {{
            gap: 0.5rem !important;
            background: transparent !important;
            border-bottom: 2px solid var(--border-color) !important;
            padding-bottom: 0px !important;
            margin-bottom: 1rem !important;
        }}

        [data-testid="stTabs"] [data-baseweb="tab"] {{
            padding: 0.65rem 1.15rem !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            color: var(--text-muted) !important;
            border-radius: 8px 8px 0 0 !important;
            background: transparent !important;
            border-bottom: 2px solid transparent !important;
            transition: var(--transition-smooth) !important;
        }}

        [data-testid="stTabs"] [data-baseweb="tab"]:hover {{
            color: var(--text-primary) !important;
            background: rgba(15, 23, 42, 0.02) !important;
        }}

        [data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {{
            color: var(--color-primary) !important;
            font-weight: 750 !important;
            border-bottom: 3px solid var(--color-primary) !important;
            background: transparent !important;
        }}

        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
            background-color: var(--color-primary) !important;
        }}


        /* ==================================================================
           STREAMLIT BUTTONS & ACTIONS
           ================================================================== */

        [data-testid="stBaseButton-secondary"],
        .stButton > button {{
            background: #FFFFFF !important;
            color: var(--text-primary) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            font-size: 12.5px !important;
            font-weight: 650 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition-smooth) !important;
        }}

        [data-testid="stBaseButton-secondary"]:hover,
        .stButton > button:hover {{
            border-color: var(--border-strong) !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
            transform: translateY(-1px) !important;
            color: var(--color-primary) !important;
        }}

        [data-testid="stBaseButton-primary"] {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
            color: #FFFFFF !important;
            border: 2px solid var(--color-primary-dark) !important;
            border-radius: var(--radius-md) !important;
            font-size: 12.5px !important;
            font-weight: 700 !important;
            padding: 0.5rem 1.15rem !important;
            box-shadow: 0 4px 14px rgba(27, 67, 50, 0.35) !important;
            transition: var(--transition-smooth) !important;
        }}

        [data-testid="stBaseButton-primary"]:hover {{
            box-shadow: 0 6px 20px rgba(27, 67, 50, 0.45) !important;
            transform: translateY(-1px) !important;
        }}


        /* ==================================================================
           STREAMLIT FORM INPUTS & SELECTBOXES
           ================================================================== */

        [data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-sm) !important;
            font-size: 13px !important;
            transition: var(--transition-smooth) !important;
        }}

        [data-baseweb="select"] > div:hover {{
            border-color: var(--border-strong) !important;
        }}

        [data-baseweb="select"] > div:focus-within {{
            border-color: var(--color-primary) !important;
            box-shadow: 0 0 0 3px rgba(27, 67, 50, 0.15) !important;
        }}

        [data-baseweb="input"] input {{
            background-color: #FFFFFF !important;
            border: 2px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            font-size: 13px !important;
        }}




        /* ==================================================================
           INTER WEB FONT IMPORT
           ================================================================== */

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');


        /* ==================================================================
           ACCESSIBILITY & REDUCED MOTION
           ================================================================== */

        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}

        :focus-visible {{
            outline: 2px solid var(--color-primary) !important;
            outline-offset: 2px !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# 6. PUBLIC API EXPORT
# ============================================================================

__all__ = [
    "COLORS",
    "CHART_PALETTE",
    "FONT_FAMILY",
    "SHADOWS",
    "RADIUS",
    "SPACING",
    "inject_global_styles",
]