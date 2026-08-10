"""
Enterprise Predictive Analytics Engine
---------------------------------------

Centralized visual design system for the Streamlit dashboard.

Design goals
------------
- Premium enterprise analytics appearance
- Dark product-navigation sidebar
- Soft analytical application canvas
- Strong blue / violet brand identity
- Layered surfaces with restrained shadows
- Professional KPI cards
- Reusable chart and panel surfaces
- Insight and status cards
- Consistent forms, buttons, tabs and tables
- Responsive behavior

All dashboard pages should consume these styles rather than
injecting their own page-specific CSS.
"""

from __future__ import annotations

import streamlit as st


# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # Application surfaces
    "background": "#F4F7FB",
    "background_top": "#F8FAFC",
    "surface": "#FFFFFF",
    "surface_soft": "#F8FAFC",
    "surface_alt": "#F1F5F9",

    # Colored surfaces
    "surface_blue": "#EFF6FF",
    "surface_violet": "#F5F3FF",
    "surface_green": "#ECFDF5",
    "surface_amber": "#FFFBEB",
    "surface_red": "#FEF2F2",

    # Borders
    "border": "#E2E8F0",
    "border_strong": "#CBD5E1",
    "border_blue": "#BFDBFE",
    "border_violet": "#DDD6FE",
    "border_green": "#A7F3D0",
    "border_amber": "#FDE68A",
    "border_red": "#FECACA",

    # Typography
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#94A3B8",
    "text_inverse": "#FFFFFF",

    # Brand
    "primary": "#2563EB",
    "primary_dark": "#1D4ED8",
    "primary_deep": "#1E3A8A",
    "primary_soft": "#EFF6FF",

    "secondary": "#7C3AED",
    "secondary_soft": "#F5F3FF",

    # Semantic colors
    "success": "#059669",
    "success_bright": "#10B981",
    "success_soft": "#ECFDF5",

    "warning": "#D97706",
    "warning_bright": "#F59E0B",
    "warning_soft": "#FFFBEB",

    "danger": "#DC2626",
    "danger_bright": "#EF4444",
    "danger_soft": "#FEF2F2",

    "info": "#0891B2",
    "info_soft": "#ECFEFF",

    # Sidebar
    "sidebar": "#0B1220",
    "sidebar_mid": "#0D1525",
    "sidebar_surface": "#111827",
    "sidebar_hover": "#172033",
    "sidebar_active": "#172B4D",
    "sidebar_text": "#CBD5E1",
    "sidebar_text_active": "#FFFFFF",
    "sidebar_muted": "#64748B",
}


# ============================================================================
# TYPOGRAPHY
# ============================================================================

FONT_FAMILY = (
    "Inter, -apple-system, BlinkMacSystemFont, "
    '"Segoe UI", sans-serif'
)


# ============================================================================
# SHADOW SYSTEM
# ============================================================================

SHADOWS = {
    "xs": "0 1px 2px rgba(15, 23, 42, 0.04)",
    "sm": "0 2px 8px rgba(15, 23, 42, 0.05)",
    "md": "0 8px 24px rgba(15, 23, 42, 0.07)",
    "lg": "0 16px 40px rgba(15, 23, 42, 0.10)",
    "blue": "0 10px 30px rgba(37, 99, 235, 0.18)",
}


# ============================================================================
# GLOBAL STYLE INJECTION
# ============================================================================

def inject_global_styles() -> None:
    """
    Inject the complete application-wide dashboard design system.

    Call this once from dashboards/app.py before rendering pages.
    """

    st.markdown(
        f"""
        <style>

        /* =====================================================================
           GLOBAL FOUNDATION
           ===================================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        *,
        *::before,
        *::after {{
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        html,
        body,
        [class*="css"] {{
            font-family: {FONT_FAMILY};
        }}

        .stApp {{
            min-height: 100vh;

            background:
                radial-gradient(
                    circle at 8% 5%,
                    rgba(59, 130, 246, 0.055) 0,
                    transparent 30%
                ),
                radial-gradient(
                    circle at 92% 88%,
                    rgba(124, 58, 237, 0.045) 0,
                    transparent 30%
                ),
                linear-gradient(
                    180deg,
                    {COLORS["background_top"]} 0%,
                    {COLORS["background"]} 48%,
                    #F1F5F9 100%
                );

            color: {COLORS["text_primary"]};
        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}

        [data-testid="block-container"] {{
            max-width: 1520px;

            padding-top: 1.5rem;
            padding-bottom: 3.5rem;

            padding-left: 2.25rem;
            padding-right: 2.25rem;
        }}

        #MainMenu,
        footer {{
            visibility: hidden;
        }}

        header {{
            background: transparent !important;
        }}


        /* =====================================================================
           TYPOGRAPHY
           ===================================================================== */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            color: {COLORS["text_primary"]} !important;
            font-weight: 750 !important;
            letter-spacing: -0.025em;
        }}

        p {{
            color: {COLORS["text_secondary"]};
        }}

        a {{
            color: {COLORS["primary"]};
        }}

        hr {{
            border: 0;
            border-top: 1px solid {COLORS["border"]};
            margin: 1.35rem 0;
        }}


        /* =====================================================================
           SIDEBAR
           ===================================================================== */

        section[data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    {COLORS["sidebar"]} 0%,
                    {COLORS["sidebar_mid"]} 55%,
                    {COLORS["sidebar"]} 100%
                );

            border-right:
                1px solid rgba(255, 255, 255, 0.055);

            box-shadow:
                8px 0 30px rgba(15, 23, 42, 0.08);
        }}

        section[data-testid="stSidebar"] > div {{
            background: transparent;
        }}

        section[data-testid="stSidebar"] * {{
            color: {COLORS["sidebar_text"]};
        }}


        /* =====================================================================
           SIDEBAR BRAND
           ===================================================================== */

        .sidebar-brand {{
            position: relative;

            margin:
                0.15rem 0.2rem 1rem 0.2rem;

            padding:
                0.8rem 0.65rem 1.2rem 0.65rem;

            border-bottom:
                1px solid rgba(255, 255, 255, 0.07);
        }}

        .sidebar-brand-row {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }}

        .sidebar-brand-mark {{
            width: 43px;
            height: 43px;

            display: inline-flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    {COLORS["primary"]},
                    {COLORS["secondary"]}
                );

            color: #FFFFFF !important;

            font-size: 17px;
            font-weight: 800;

            box-shadow:
                {SHADOWS["blue"]};
        }}

        .sidebar-brand-title {{
            color: #FFFFFF !important;

            font-size: 14px;
            font-weight: 750;

            letter-spacing: 0.01em;
            line-height: 1.2;
        }}

        .sidebar-brand-subtitle {{
            margin-top: 0.22rem;

            color:
                {COLORS["sidebar_muted"]} !important;

            font-size: 10px;
            line-height: 1.45;
        }}


        /* =====================================================================
           SIDEBAR NAVIGATION
           ===================================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] {{
            padding:
                0.1rem 0.55rem 1rem 0.55rem;
        }}

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] ul {{
            gap: 0.18rem;
        }}

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] li > div {{
            padding:
                0.65rem 0.75rem 0.3rem 0.75rem;

            color:
                {COLORS["sidebar_muted"]} !important;

            font-size: 9px;
            font-weight: 750;

            text-transform: uppercase;
            letter-spacing: 0.095em;
        }}

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a {{
            position: relative;

            min-height: 43px;

            padding:
                0.58rem 0.72rem;

            border-radius: 11px;

            color:
                {COLORS["sidebar_text"]} !important;

            font-size: 12px;
            font-weight: 550;

            transition:
                background 150ms ease,
                color 150ms ease,
                transform 150ms ease,
                box-shadow 150ms ease;
        }}

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a:hover {{
            background:
                rgba(255, 255, 255, 0.055);

            color:
                #FFFFFF !important;

            transform:
                translateX(2px);
        }}

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] {{
            background:
                linear-gradient(
                    90deg,
                    rgba(37, 99, 235, 0.27),
                    rgba(124, 58, 237, 0.10)
                );

            color:
                #FFFFFF !important;

            font-weight: 700;

            box-shadow:
                inset 3px 0 0 {COLORS["primary"]},
                0 5px 16px rgba(0, 0, 0, 0.10);
        }}

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a svg {{
            width: 17px;
            height: 17px;

            margin-right: 0.5rem;
        }}


        /* =====================================================================
           SIDEBAR FOOTER
           ===================================================================== */

        .sidebar-footer {{
            margin:
                1.4rem 0.55rem 0.4rem 0.55rem;

            padding:
                0.85rem 0.9rem;

            background:
                rgba(255, 255, 255, 0.035);

            border:
                1px solid rgba(255, 255, 255, 0.06);

            border-radius: 12px;
        }}

        .sidebar-footer-status {{
            display: flex;
            align-items: center;

            gap: 0.45rem;

            color: #A7F3D0 !important;

            font-size: 9px;
            font-weight: 750;

            letter-spacing: 0.07em;
            text-transform: uppercase;
        }}

        .sidebar-status-dot {{
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background:
                #34D399;

            box-shadow:
                0 0 0 4px rgba(52, 211, 153, 0.10);
        }}

        .sidebar-footer-product {{
            margin-top: 0.5rem;

            color: #CBD5E1 !important;

            font-size: 10px;
            line-height: 1.45;
        }}

        .sidebar-footer-version {{
            margin-top: 0.25rem;

            color: #64748B !important;

            font-size: 9px;
        }}


        /* =====================================================================
           PAGE HEADER
           ===================================================================== */

        .page-header {{
            position: relative;

            display: flex;

            align-items: flex-start;
            justify-content: space-between;

            gap: 1.5rem;

            margin-bottom: 1.35rem;

            padding:
                1.35rem 1.45rem 1.25rem 1.45rem;

            background:
                linear-gradient(
                    135deg,
                    rgba(239, 246, 255, 0.96),
                    rgba(255, 255, 255, 0.98) 55%,
                    rgba(245, 243, 255, 0.94)
                );

            border:
                1px solid #DCE7F7;

            border-radius: 18px;

            box-shadow:
                {SHADOWS["sm"]};

            overflow: hidden;
        }}

        .page-header::after {{
            content: "";

            position: absolute;

            width: 240px;
            height: 240px;

            right: -100px;
            top: -150px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(59, 130, 246, 0.11),
                    transparent 68%
                );

            pointer-events: none;
        }}

        .page-header-content {{
            position: relative;

            z-index: 1;

            min-width: 0;
        }}

        .page-header-title {{
            margin: 0;

            color:
                {COLORS["text_primary"]};

            font-size: 30px;
            font-weight: 800;

            letter-spacing: -0.045em;
            line-height: 1.1;
        }}

        .page-header-description {{
            max-width: 900px;

            margin-top: 0.45rem;

            color:
                {COLORS["text_secondary"]};

            font-size: 12px;
            line-height: 1.6;
        }}

        .page-header-status {{
            position: relative;

            z-index: 1;

            flex-shrink: 0;

            padding-top: 0.1rem;
        }}


        /* =====================================================================
           STATUS BADGES
           ===================================================================== */

        .status-badge {{
            display: inline-flex;

            align-items: center;
            justify-content: center;

            gap: 0.35rem;

            padding:
                0.35rem 0.7rem;

            border-radius: 999px;

            font-size: 9px;
            font-weight: 750;

            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .status-live {{
            color:
                {COLORS["success"]};

            background:
                {COLORS["success_soft"]};

            border:
                1px solid rgba(5, 150, 105, 0.14);
        }}

        .status-warning {{
            color:
                {COLORS["warning"]};

            background:
                {COLORS["warning_soft"]};

            border:
                1px solid rgba(217, 119, 6, 0.14);
        }}

        .status-danger {{
            color:
                {COLORS["danger"]};

            background:
                {COLORS["danger_soft"]};

            border:
                1px solid rgba(220, 38, 38, 0.14);
        }}

        .status-info {{
            color:
                {COLORS["info"]};

            background:
                {COLORS["info_soft"]};

            border:
                1px solid rgba(8, 145, 178, 0.14);
        }}


        /* =====================================================================
           KPI CARDS
           ===================================================================== */

        .kpi-grid {{
            display: grid;

            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 0.9rem;
        }}

        .kpi-card {{
            position: relative;

            min-height: 142px;

            overflow: hidden;

            padding:
                1.15rem 1.2rem;

            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 16px;

            box-shadow:
                {SHADOWS["xs"]};

            transition:
                transform 170ms ease,
                border-color 170ms ease,
                box-shadow 170ms ease;
        }}

        .kpi-card::before {{
            content: "";

            position: absolute;

            top: 0;
            left: 0;

            width: 100%;
            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    {COLORS["primary"]},
                    #60A5FA
                );
        }}

        .kpi-card::after {{
            content: "";

            position: absolute;

            width: 150px;
            height: 150px;

            right: -85px;
            top: -90px;

            border-radius: 50%;

            background:
                rgba(59, 130, 246, 0.045);

            pointer-events: none;
        }}

        .kpi-card:hover {{
            transform:
                translateY(-3px);

            border-color:
                #C8D5E6;

            box-shadow:
                {SHADOWS["md"]};
        }}

        .kpi-label {{
            color:
                {COLORS["text_secondary"]};

            font-size: 9px;
            font-weight: 750;

            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .kpi-value {{
            margin-top: 0.5rem;

            color:
                {COLORS["text_primary"]};

            font-size: 27px;
            font-weight: 800;

            letter-spacing: -0.045em;
            line-height: 1.15;
        }}

        .kpi-footer {{
            display: flex;

            align-items: center;

            min-height: 18px;

            margin-top: 0.55rem;

            font-size: 10px;
        }}

        .kpi-positive {{
            color:
                {COLORS["success"]};

            font-weight: 650;
        }}

        .kpi-negative {{
            color:
                {COLORS["danger"]};

            font-weight: 650;
        }}

        .kpi-neutral {{
            color:
                {COLORS["text_muted"]};

            font-weight: 550;
        }}

        .kpi-blue::before {{
            background:
                linear-gradient(
                    90deg,
                    #1D4ED8,
                    #60A5FA
                );
        }}

        .kpi-green::before {{
            background:
                linear-gradient(
                    90deg,
                    #047857,
                    #34D399
                );
        }}

        .kpi-purple::before {{
            background:
                linear-gradient(
                    90deg,
                    #6D28D9,
                    #A78BFA
                );
        }}

        .kpi-amber::before {{
            background:
                linear-gradient(
                    90deg,
                    #B45309,
                    #FBBF24
                );
        }}

        .kpi-red::before {{
            background:
                linear-gradient(
                    90deg,
                    #B91C1C,
                    #F87171
                );
        }}


        /* =====================================================================
           SECTION HEADERS
           ===================================================================== */

        .section-header {{
            position: relative;

            margin-top: 1.8rem;
            margin-bottom: 0.85rem;

            padding-left: 0.85rem;
        }}

        .section-header::before {{
            content: "";

            position: absolute;

            left: 0;
            top: 2px;

            width: 4px;
            height: 31px;

            border-radius: 999px;

            background:
                linear-gradient(
                    180deg,
                    {COLORS["primary"]},
                    {COLORS["secondary"]}
                );

            box-shadow:
                0 2px 8px rgba(37, 99, 235, 0.20);
        }}

        .section-title {{
            color:
                {COLORS["text_primary"]};

            font-size: 17px;
            font-weight: 750;

            letter-spacing: -0.025em;

            line-height: 1.25;
        }}

        .section-description {{
            margin-top: 0.2rem;

            color:
                {COLORS["text_secondary"]};

            font-size: 11px;
            line-height: 1.5;
        }}

        .subsection-header {{
            margin-top: 1rem;
            margin-bottom: 0.6rem;
        }}

        .subsection-title {{
            color:
                {COLORS["text_primary"]};

            font-size: 13px;
            font-weight: 700;

            letter-spacing: -0.015em;
        }}

        .subsection-description {{
            margin-top: 0.18rem;

            color:
                {COLORS["text_secondary"]};

            font-size: 10px;
        }}


        /* =====================================================================
           ANALYTICAL PANELS
           ===================================================================== */

        .dashboard-panel,
        .chart-card {{
            position: relative;

            width: 100%;

            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 16px;

            box-shadow:
                {SHADOWS["xs"]};

            overflow: hidden;
        }}

        .dashboard-panel {{
            padding:
                1.05rem 1.1rem 0.85rem 1.1rem;
        }}

        .chart-card {{
            padding:
                1rem 1.05rem 0.7rem 1.05rem;

            transition:
                box-shadow 180ms ease,
                transform 180ms ease,
                border-color 180ms ease;
        }}

        .chart-card:hover {{
            transform:
                translateY(-1px);

            border-color:
                #D4DEE9;

            box-shadow:
                {SHADOWS["sm"]};
        }}

        .dashboard-panel-title,
        .chart-card-title {{
            color:
                {COLORS["text_primary"]};

            font-size: 13px;
            font-weight: 700;

            letter-spacing: -0.015em;
        }}

        .dashboard-panel-description,
        .chart-card-desc {{
            margin-top: 0.2rem;

            color:
                {COLORS["text_secondary"]};

            font-size: 10px;
            line-height: 1.5;
        }}

        .chart-container {{
            width: 100%;

            margin-top: 0.55rem;

            padding: 0.25rem;

            background:
                #FFFFFF;

            border-radius: 12px;

            overflow: hidden;
        }}


        /* =====================================================================
           VISUAL CARD SYSTEM
           ===================================================================== */

        .card-surface {{
            position: relative;

            overflow: hidden;

            padding:
                1.25rem 1.35rem;

            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 17px;

            box-shadow:
                {SHADOWS["xs"]};

            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                border-color 180ms ease;
        }}

        .card-surface:hover {{
            transform:
                translateY(-2px);

            border-color:
                #CBD5E1;

            box-shadow:
                {SHADOWS["md"]};
        }}

        .card-gradient-blue {{
            background:
                linear-gradient(
                    135deg,
                    #EFF6FF 0%,
                    #FFFFFF 68%
                );

            border-color:
                {COLORS["border_blue"]};
        }}

        .card-gradient-green {{
            background:
                linear-gradient(
                    135deg,
                    #ECFDF5 0%,
                    #FFFFFF 68%
                );

            border-color:
                {COLORS["border_green"]};
        }}

        .card-gradient-purple {{
            background:
                linear-gradient(
                    135deg,
                    #F5F3FF 0%,
                    #FFFFFF 68%
                );

            border-color:
                {COLORS["border_violet"]};
        }}

        .card-gradient-amber {{
            background:
                linear-gradient(
                    135deg,
                    #FFFBEB 0%,
                    #FFFFFF 68%
                );

            border-color:
                {COLORS["border_amber"]};
        }}

        .card-gradient-red {{
            background:
                linear-gradient(
                    135deg,
                    #FEF2F2 0%,
                    #FFFFFF 68%
                );

            border-color:
                {COLORS["border_red"]};
        }}

        .card-header {{
            display: flex;

            align-items: center;

            gap: 0.75rem;

            margin-bottom: 0.75rem;
        }}

        .card-icon {{
            width: 43px;
            height: 43px;

            display: inline-flex;

            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 12px;

            color:
                #FFFFFF !important;

            font-size: 1.15rem;

            box-shadow:
                0 5px 14px rgba(15, 23, 42, 0.12);
        }}

        .card-icon-blue {{
            background:
                linear-gradient(
                    135deg,
                    #1E40AF,
                    #3B82F6
                );
        }}

        .card-icon-green {{
            background:
                linear-gradient(
                    135deg,
                    #047857,
                    #10B981
                );
        }}

        .card-icon-purple {{
            background:
                linear-gradient(
                    135deg,
                    #6D28D9,
                    #8B5CF6
                );
        }}

        .card-icon-amber {{
            background:
                linear-gradient(
                    135deg,
                    #B45309,
                    #F59E0B
                );
        }}

        .card-icon-red {{
            background:
                linear-gradient(
                    135deg,
                    #B91C1C,
                    #EF4444
                );
        }}

        .card-title {{
            color:
                {COLORS["text_secondary"]};

            font-size: 9px;
            font-weight: 700;

            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .card-value {{
            margin-top: 0.15rem;

            color:
                {COLORS["text_primary"]};

            font-size: 25px;
            font-weight: 800;

            letter-spacing: -0.04em;

            line-height: 1.15;
        }}

        .card-subtitle {{
            margin-top: 0.28rem;

            color:
                {COLORS["text_secondary"]};

            font-size: 10px;

            line-height: 1.5;
        }}


        /* =====================================================================
           INSIGHT CARDS
           ===================================================================== */

        .insight-card {{
            position: relative;

            min-height: 125px;

            padding:
                1rem 1.1rem 1rem 1.15rem;

            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 15px;

            box-shadow:
                {SHADOWS["xs"]};

            overflow: hidden;
        }}

        .insight-card::before {{
            content: "";

            position: absolute;

            left: 0;
            top: 0;
            bottom: 0;

            width: 4px;

            background:
                {COLORS["primary"]};
        }}

        .insight-card-blue::before {{
            background:
                linear-gradient(
                    180deg,
                    #1D4ED8,
                    #60A5FA
                );
        }}

        .insight-card-green::before {{
            background:
                linear-gradient(
                    180deg,
                    #047857,
                    #34D399
                );
        }}

        .insight-card-amber::before {{
            background:
                linear-gradient(
                    180deg,
                    #B45309,
                    #FBBF24
                );
        }}

        .insight-card-red::before {{
            background:
                linear-gradient(
                    180deg,
                    #B91C1C,
                    #F87171
                );
        }}

        .insight-card-purple::before {{
            background:
                linear-gradient(
                    180deg,
                    #6D28D9,
                    #A78BFA
                );
        }}

        .insight-label {{
            font-size: 9px;

            font-weight: 800;

            text-transform: uppercase;

            letter-spacing: 0.08em;
        }}

        .insight-title {{
            margin-top: 0.35rem;

            color:
                {COLORS["text_primary"]};

            font-size: 13px;

            font-weight: 720;

            line-height: 1.35;
        }}

        .insight-description {{
            margin-top: 0.38rem;

            color:
                {COLORS["text_secondary"]};

            font-size: 10px;

            line-height: 1.55;
        }}

        .insight-danger {{
            color:
                {COLORS["danger"]};
        }}

        .insight-warning {{
            color:
                {COLORS["warning"]};
        }}

        .insight-success {{
            color:
                {COLORS["success"]};
        }}

        .insight-info {{
            color:
                {COLORS["info"]};
        }}

        .insight-purple {{
            color:
                {COLORS["secondary"]};
        }}


        /* =====================================================================
           STATUS / RISK BANNERS
           ===================================================================== */

        .status-banner {{
            position: relative;

            overflow: hidden;

            display: flex;

            align-items: flex-start;

            gap: 0.9rem;

            padding:
                1.15rem 1.25rem;

            margin-bottom: 1rem;

            border-radius: 16px;

            color:
                #FFFFFF !important;

            box-shadow:
                {SHADOWS["md"]};
        }}

        .status-banner::after {{
            content: "";

            position: absolute;

            width: 260px;
            height: 260px;

            right: -110px;
            top: -130px;

            border-radius: 50%;

            background:
                rgba(255, 255, 255, 0.12);

            pointer-events: none;
        }}

        .status-banner-risk-low {{
            background:
                linear-gradient(
                    135deg,
                    #047857,
                    #059669 50%,
                    #10B981
                );
        }}

        .status-banner-risk-medium {{
            background:
                linear-gradient(
                    135deg,
                    #B45309,
                    #D97706 50%,
                    #F59E0B
                );
        }}

        .status-banner-risk-high {{
            background:
                linear-gradient(
                    135deg,
                    #B91C1C,
                    #DC2626 50%,
                    #EF4444
                );
        }}

        .status-banner-icon {{
            position: relative;

            z-index: 1;

            width: 45px;
            height: 45px;

            display: inline-flex;

            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 13px;

            background:
                rgba(255, 255, 255, 0.17);

            color:
                #FFFFFF !important;

            font-size: 1.25rem;

            backdrop-filter:
                blur(6px);
        }}

        .status-banner-content {{
            position: relative;

            z-index: 1;

            flex: 1;
        }}

        .status-banner-label {{
            font-size: 8px;

            font-weight: 800;

            letter-spacing: 0.09em;

            text-transform: uppercase;

            opacity: 0.9;
        }}

        .status-banner-title {{
            margin-top: 0.18rem;

            color:
                #FFFFFF !important;

            font-size: 18px;

            font-weight: 800;

            line-height: 1.2;
        }}

        .status-banner-desc {{
            margin-top: 0.25rem;

            color:
                rgba(255,255,255,0.90) !important;

            font-size: 10px;

            line-height: 1.5;
        }}


        /* =====================================================================
           PROBABILITY GAUGE
           ===================================================================== */

        .probability-gauge {{
            padding:
                1.2rem 1.35rem;

            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 17px;

            box-shadow:
                {SHADOWS["xs"]};

            text-align: center;
        }}

        .probability-gauge-label {{
            color:
                {COLORS["text_secondary"]};

            font-size: 9px;

            font-weight: 700;

            letter-spacing: 0.06em;

            text-transform: uppercase;
        }}

        .probability-gauge-value {{
            margin-top: 0.45rem;

            color:
                {COLORS["text_primary"]};

            font-size: 42px;

            font-weight: 850;

            letter-spacing: -0.055em;

            line-height: 1;
        }}

        .probability-bar-outer {{
            height: 13px;

            margin:
                0.9rem 0 0.45rem;

            background:
                #E2E8F0;

            border-radius: 999px;

            overflow: hidden;

            box-shadow:
                inset 0 1px 3px rgba(15,23,42,0.08);
        }}

        .probability-bar-inner {{
            height: 100%;

            border-radius: 999px;

            position: relative;

            transition:
                width 700ms ease;
        }}

        .probability-bar-inner::after {{
            content: "";

            position: absolute;

            inset: 0;

            background:
                linear-gradient(
                    90deg,
                    rgba(255,255,255,0.24),
                    transparent 55%
                );
        }}

        .probability-bar-low {{
            background:
                linear-gradient(
                    90deg,
                    #059669,
                    #10B981
                );
        }}

        .probability-bar-medium {{
            background:
                linear-gradient(
                    90deg,
                    #D97706,
                    #F59E0B
                );
        }}

        .probability-bar-high {{
            background:
                linear-gradient(
                    90deg,
                    #DC2626,
                    #EF4444
                );
        }}

        .probability-scale {{
            display: flex;

            justify-content: space-between;

            color:
                {COLORS["text_muted"]};

            font-size: 8px;

            font-weight: 600;
        }}


        /* =====================================================================
           PILLS / TAGS
           ===================================================================== */

        .pill {{
            display: inline-flex;

            align-items: center;

            gap: 0.3rem;

            padding:
                0.28rem 0.68rem;

            border-radius: 999px;

            font-size: 9px;

            font-weight: 700;
        }}

        .pill-blue {{
            color: #1D4ED8;
            background: #DBEAFE;
        }}

        .pill-green {{
            color: #047857;
            background: #D1FAE5;
        }}

        .pill-purple {{
            color: #6D28D9;
            background: #EDE9FE;
        }}

        .pill-amber {{
            color: #B45309;
            background: #FEF3C7;
        }}

        .pill-red {{
            color: #B91C1C;
            background: #FEE2E2;
        }}

        .pill-gray {{
            color: #475569;
            background: #F1F5F9;
        }}


        /* =====================================================================
           DATA TABLES
           ===================================================================== */

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {{
            border:
                1px solid {COLORS["border"]};

            border-radius: 14px;

            overflow: hidden;

            background:
                #FFFFFF;

            box-shadow:
                {SHADOWS["xs"]};
        }}

        [data-testid="stDataFrame"] th,
        [data-testid="stTable"] th {{
            background:
                #F8FAFC !important;

            color:
                {COLORS["text_secondary"]} !important;

            font-size: 10px !important;

            font-weight: 700 !important;
        }}

        [data-testid="stDataFrame"] td,
        [data-testid="stTable"] td {{
            color:
                {COLORS["text_secondary"]} !important;

            font-size: 10px !important;
        }}


        /* =====================================================================
           BUTTONS
           ===================================================================== */

        .stButton > button,
        .stDownloadButton > button {{
            min-height: 38px;

            padding:
                0.45rem 0.9rem;

            border:
                1px solid {COLORS["border"]};

            border-radius: 10px;

            background:
                #FFFFFF;

            color:
                {COLORS["text_primary"]};

            font-size: 11px;

            font-weight: 650;

            transition:
                transform 150ms ease,
                border-color 150ms ease,
                box-shadow 150ms ease,
                background 150ms ease;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            border-color:
                {COLORS["primary"]};

            background:
                {COLORS["primary_soft"]};

            color:
                {COLORS["primary_dark"]};

            transform:
                translateY(-1px);

            box-shadow:
                0 5px 14px rgba(37, 99, 235, 0.12);
        }}

        .stButton > button[kind="primary"] {{
            border:
                0;

            background:
                linear-gradient(
                    135deg,
                    {COLORS["primary_dark"]},
                    {COLORS["primary"]}
                );

            color:
                #FFFFFF !important;

            box-shadow:
                0 5px 16px rgba(37, 99, 235, 0.20);
        }}

        .stButton > button[kind="primary"]:hover {{
            color:
                #FFFFFF !important;

            background:
                linear-gradient(
                    135deg,
                    #1E3A8A,
                    #2563EB
                );
        }}


        /* =====================================================================
           INPUTS
           ===================================================================== */

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            min-height: 40px;

            border:
                1px solid {COLORS["border"]};

            border-radius: 10px;

            background:
                #FFFFFF;

            box-shadow:
                none;
        }}

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="input"] > div:hover {{
            border-color:
                {COLORS["border_strong"]};
        }}

        input,
        textarea {{
            font-family:
                {FONT_FAMILY} !important;

            color:
                {COLORS["text_primary"]} !important;
        }}

        label {{
            color:
                {COLORS["text_secondary"]} !important;

            font-size: 10px !important;

            font-weight: 650 !important;
        }}


        /* =====================================================================
           TABS
           ===================================================================== */

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.3rem;

            padding:
                0.25rem;

            background:
                {COLORS["surface_alt"]};

            border:
                1px solid {COLORS["border"]};

            border-radius: 11px;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding:
                0.45rem 0.82rem;

            border-radius: 8px;

            color:
                {COLORS["text_secondary"]};

            font-size: 10px;

            font-weight: 650;
        }}

        .stTabs [aria-selected="true"] {{
            background:
                #FFFFFF !important;

            color:
                {COLORS["primary_dark"]} !important;

            box-shadow:
                {SHADOWS["xs"]};
        }}


        /* =====================================================================
           STREAMLIT METRICS
           ===================================================================== */

        [data-testid="stMetric"] {{
            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 14px;

            padding:
                0.85rem 1rem;

            box-shadow:
                {SHADOWS["xs"]};
        }}


        /* =====================================================================
           EXPANDERS
           ===================================================================== */

        [data-testid="stExpander"] {{
            border:
                1px solid {COLORS["border"]};

            border-radius: 13px;

            background:
                #FFFFFF;

            box-shadow:
                {SHADOWS["xs"]};
        }}


        /* =====================================================================
           FORMS
           ===================================================================== */

        [data-testid="stForm"] {{
            background:
                #FFFFFF;

            border:
                1px solid {COLORS["border"]};

            border-radius: 16px;

            padding:
                1.2rem 1.35rem;

            box-shadow:
                {SHADOWS["xs"]};
        }}


        /* =====================================================================
           LAYOUT HELPERS
           ===================================================================== */

        .grid-2 {{
            display: grid;

            grid-template-columns:
                repeat(2, minmax(0, 1fr));

            gap: 1rem;
        }}

        .grid-3 {{
            display: grid;

            grid-template-columns:
                repeat(3, minmax(0, 1fr));

            gap: 1rem;
        }}

        .grid-4 {{
            display: grid;

            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 0.9rem;
        }}

        .two-col-layout {{
            display: grid;

            grid-template-columns:
                minmax(0, 1fr)
                minmax(0, 1fr);

            gap: 1rem;
        }}


        /* =====================================================================
           RESPONSIVE DESIGN
           ===================================================================== */

        @media (max-width: 1150px) {{

            [data-testid="block-container"] {{
                padding-left: 1.4rem;
                padding-right: 1.4rem;
            }}

            .grid-4,
            .kpi-grid {{
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }}

            .grid-3 {{
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 850px) {{

            [data-testid="block-container"] {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .page-header {{
                flex-direction: column;
                gap: 0.7rem;
            }}

            .page-header-title {{
                font-size: 25px;
            }}

            .grid-2,
            .grid-3,
            .grid-4,
            .kpi-grid,
            .two-col-layout {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 600px) {{

            [data-testid="block-container"] {{
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }}

            .page-header {{
                padding: 1rem;
                border-radius: 14px;
            }}

            .page-header-title {{
                font-size: 22px;
            }}

            .kpi-card {{
                min-height: 125px;
            }}

            .kpi-value {{
                font-size: 23px;
            }}

            .status-banner {{
                padding: 0.95rem;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )