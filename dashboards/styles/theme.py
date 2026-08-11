"""
Enterprise Dashboard Design System
-----------------------------------

Centralized visual system for the Enterprise Predictive Analytics Engine.

This module controls:

- Global application styling
- Typography
- Sidebar navigation
- Custom page-link navigation
- KPI cards
- Section headers
- Charts
- Tables
- Buttons
- Tabs
- Alerts
- Responsive behavior
- Accessibility states

The application uses a light analytical canvas with a dark,
professional navigation sidebar.
"""

from __future__ import annotations

import streamlit as st


# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # Application (Light Grey / Soft Canvas)
    "background": "#F8FAFC",
    "background_top": "#F0F9FF",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFC",
    "surface_soft": "#F1F5F9",

    # Sidebar (Light Sky Blue Canvas)
    "sidebar": "#F0F9FF",
    "sidebar_surface": "#E0F2FE",
    "sidebar_hover": "#BAE6FD",
    "sidebar_active": "#0EA5E9",

    # Primary (Sky Blue)
    "primary": "#0EA5E9",
    "primary_dark": "#0284C7",
    "primary_light": "#E0F2FE",
    "primary_soft": "#F0F9FF",

    # Secondary (Light Purple / Lavender)
    "secondary": "#A855F7",
    "secondary_dark": "#7E22CE",
    "secondary_light": "#F3E8FF",
    "secondary_soft": "#FAF5FF",

    # Success
    "success": "#10B981",
    "success_dark": "#059669",
    "success_light": "#D1FAE5",
    "success_soft": "#ECFDF5",

    # Warning
    "warning": "#F59E0B",
    "warning_dark": "#D97706",
    "warning_light": "#FEF3C7",
    "warning_soft": "#FFFBEB",

    # Danger
    "danger": "#EF4444",
    "danger_dark": "#DC2626",
    "danger_light": "#FEE2E2",
    "danger_soft": "#FEF2F2",

    # Information (Sky)
    "info": "#38BDF8",
    "info_dark": "#0284C7",
    "info_light": "#E0F2FE",
    "info_soft": "#F0F9FF",

    # Text
    "text": "#0F172A",
    "text_secondary": "#334155",
    "text_muted": "#64748B",
    "text_light": "#94A3B8",
    "text_inverse": "#FFFFFF",

    # Borders (Light Grey)
    "border": "#E2E8F0",
    "border_light": "#F1F5F9",
    "border_strong": "#CBD5E1",

    # Charts (Sky Blue, Light Purple, Mint, Amber, Rose)
    "chart_blue": "#0EA5E9",
    "chart_purple": "#A855F7",
    "chart_green": "#10B981",
    "chart_amber": "#F59E0B",
    "chart_red": "#EF4444",
    "chart_cyan": "#38BDF8",
    "chart_pink": "#EC4899",
    "chart_indigo": "#6366F1",
    "chart_teal": "#14B8A6",
    "chart_violet": "#C084FC",

    # Miscellaneous
    "white": "#FFFFFF",
    "black": "#000000",
    "transparent": "rgba(0,0,0,0)",
}


# ============================================================================
# TYPOGRAPHY
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
# SHADOWS
# ============================================================================

SHADOWS = {
    "none": "none",
    "sm": "0 1px 2px rgba(15, 23, 42, 0.04)",
    "card": "0 2px 8px rgba(15, 23, 42, 0.04)",
    "card_hover": "0 8px 24px rgba(15, 23, 42, 0.08)",
    "md": "0 8px 24px rgba(15, 23, 42, 0.08)",
    "lg": "0 16px 40px rgba(15, 23, 42, 0.12)",
}


# ============================================================================
# BORDER RADIUS
# ============================================================================

RADIUS = {
    "sm": "6px",
    "md": "10px",
    "lg": "14px",
    "xl": "18px",
    "pill": "999px",
}


# ============================================================================
# SPACING
# ============================================================================

SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "0.75rem",
    "lg": "1rem",
    "xl": "1.5rem",
    "xxl": "2rem",
    "section": "2.25rem",
}


# ============================================================================
# CHART PALETTE
# ============================================================================

CHART_PALETTE = [
    COLORS["chart_blue"],
    COLORS["chart_purple"],
    COLORS["chart_green"],
    COLORS["chart_amber"],
    COLORS["chart_red"],
    COLORS["chart_cyan"],
    COLORS["chart_pink"],
    COLORS["chart_indigo"],
    COLORS["chart_teal"],
    COLORS["chart_violet"],
]


# ============================================================================
# GLOBAL STYLE INJECTION
# ============================================================================

def inject_global_styles() -> None:
    """
    Inject the centralized dashboard design system.

    Call this once from dashboards/app.py before rendering pages.
    """

    st.markdown(
        f"""
        <style>

        /* ==================================================================
           ROOT APPLICATION
           ================================================================== */

        html,
        body {{
            background:
                {COLORS["background"]} !important;
        }}

        html,
        body,
        [class*="css"] {{
            font-family:
                {FONT_FAMILY};
        }}

        .stApp {{
            background:
                linear-gradient(
                    180deg,
                    {COLORS["background_top"]} 0%,
                    {COLORS["background"]} 48%,
                    #F1F5F9 100%
                ) !important;

            color:
                {COLORS["text"]};
        }}


        /* ==================================================================
           MAIN CONTENT CANVAS (OFFSET BY FIXED 320PX SIDEBAR)
           ================================================================== */

        [data-testid="stAppViewContainer"] {{
            background:
                {COLORS["background"]} !important;

            overflow-x:
                hidden !important;

            max-width:
                100% !important;
        }}

        [data-testid="stMain"],
        .stMain {{
            margin-left:
                320px !important;

            width:
                calc(100% - 320px) !important;

            max-width:
                calc(100% - 320px) !important;

            background:
                linear-gradient(
                    180deg,
                    {COLORS["background_top"]} 0%,
                    {COLORS["background"]} 48%,
                    #F1F5F9 100%
                ) !important;

            overflow-x:
                hidden !important;

            box-sizing:
                border-box !important;
        }}

        [data-testid="stMainBlockContainer"] {{
            background:
                transparent !important;

            overflow-x:
                hidden !important;

            max-width:
                100% !important;
        }}

        [data-testid="block-container"] {{
            max-width:
                1440px !important;

            width:
                100% !important;

            margin:
                0 auto !important;

            background:
                transparent !important;

            padding-top:
                1.5rem !important;

            padding-right:
                2rem !important;

            padding-bottom:
                3rem !important;

            padding-left:
                2rem !important;

            overflow-x:
                hidden !important;

            box-sizing:
                border-box !important;
        }}


        /* ==================================================================
           MAIN CONTENT TYPOGRAPHY
           ================================================================== */

        .stApp p {{
            color:
                {COLORS["text_secondary"]};
        }}

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {{
            color:
                {COLORS["text"]};
        }}


        /* ==================================================================
           SIDEBAR (FIXED 320PX ENTERPRISE NAVIGATION PANEL - ZERO SCROLLBARS)
           ================================================================== */

        section[data-testid="stSidebar"],
        [data-testid="stSidebar"] {{
            position:
                fixed !important;

            top:
                0 !important;

            left:
                0 !important;

            bottom:
                0 !important;

            width:
                320px !important;

            min-width:
                320px !important;

            max-width:
                320px !important;

            height:
                100vh !important;

            min-height:
                100vh !important;

            max-height:
                100vh !important;

            background:
                linear-gradient(
                    180deg,
                    #F0F9FF 0%,
                    #E0F2FE 35%,
                    #F5F3FF 75%,
                    #F8FAFC 100%
                ) !important;

            background-color:
                #F0F9FF !important;

            backdrop-filter:
                blur(20px) !important;

            -webkit-backdrop-filter:
                blur(20px) !important;

            border-right:
                1px solid rgba(186, 230, 253, 0.9) !important;

            box-shadow:
                4px 0 24px -2px rgba(14, 165, 233, 0.08),
                8px 0 36px -4px rgba(168, 85, 247, 0.05) !important;

            overflow:
                hidden !important;

            overflow-x:
                hidden !important;

            overflow-y:
                hidden !important;

            scrollbar-width:
                none !important;

            -ms-overflow-style:
                none !important;

            z-index:
                100 !important;
        }}

        /* Completely suppress all scrollbars and sliders across sidebar elements */
        section[data-testid="stSidebar"]::-webkit-scrollbar,
        [data-testid="stSidebarContent"]::-webkit-scrollbar,
        [data-testid="stSidebarUserContent"]::-webkit-scrollbar,
        [data-testid="stSidebar"]::-webkit-scrollbar,
        [data-testid="stSidebar"] *::-webkit-scrollbar,
        .sidebar-header-region::-webkit-scrollbar,
        .sidebar-footer-region::-webkit-scrollbar {{
            display:
                none !important;

            width:
                0px !important;

            height:
                0px !important;

            background:
                transparent !important;
        }}

        [data-testid="stSidebarContent"],
        [data-testid="stSidebarUserContent"] {{
            height:
                100vh !important;

            min-height:
                100vh !important;

            max-height:
                100vh !important;

            width:
                100% !important;

            max-width:
                100% !important;

            box-sizing:
                border-box !important;

            padding:
                0.75rem 0.85rem 0.75rem 0.85rem !important;

            overflow-y:
                auto !important;

            overflow-x:
                hidden !important;

            background:
                transparent !important;

            scrollbar-width:
                none !important;

            -ms-overflow-style:
                none !important;
        }}

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]:first-child {{
            height:
                auto !important;

            min-height:
                100% !important;

            width:
                100% !important;

            max-width:
                100% !important;

            display:
                flex !important;

            flex-direction:
                column !important;

            justify-content:
                flex-start !important;

            gap:
                0.1rem !important;

            box-sizing:
                border-box !important;
        }}

        [data-testid="stSidebar"] [data-testid="element-container"],
        [data-testid="stSidebar"] .stMarkdown {{
            width:
                100% !important;

            max-width:
                100% !important;

            box-sizing:
                border-box !important;

            margin:
                0 !important;

            padding:
                0 !important;

            display:
                block !important;
        }}

        [data-testid="stSidebar"] [data-testid="element-container"]:last-child {{
            margin-top:
                auto !important;

            padding-top:
                0.5rem !important;
        }}

        [data-testid="stSidebar"] * {{
            box-sizing:
                border-box !important;

            max-width:
                100% !important;

            color:
                #0F172A;
        }}

        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {{
            color:
                #0F172A;
        }}


        /* ==================================================================
           CUSTOM SIDEBAR BRAND (FUTURISTIC 3D GLOW)
           ================================================================== */

        .custom-sidebar-brand {{
            width:
                100% !important;

            max-width:
                100% !important;

            box-sizing:
                border-box !important;

            display:
                flex;

            align-items:
                center;

            gap:
                0.75rem;

            padding:
                0.6rem
                0.8rem;

            margin-bottom:
                0.25rem;

            background:
                rgba(255, 255, 255, 0.95);

            backdrop-filter:
                blur(16px);

            -webkit-backdrop-filter:
                blur(16px);

            border:
                1px solid rgba(186, 230, 253, 0.95);

            border-radius:
                13px;

            box-shadow:
                0 4px 16px rgba(14, 165, 233, 0.08),
                0 1px 3px rgba(15, 23, 42, 0.04);
        }}

        .sidebar-brand-mark {{
            width:
                40px;

            height:
                40px;

            flex-shrink:
                0;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                11px;

            background:
                linear-gradient(
                    135deg,
                    #0EA5E9 0%,
                    #8B5CF6 100%
                );

            border:
                1px solid rgba(255, 255, 255, 0.6);

            color:
                #FFFFFF;

            font-size:
                18px;

            font-weight:
                900;

            box-shadow:
                0 4px 14px rgba(14, 165, 233, 0.40),
                0 0 10px rgba(139, 92, 246, 0.28);
        }}

        .sidebar-brand-text {{
            min-width:
                0;
        }}

        .sidebar-brand-title {{
            color:
                #0F172A !important;

            font-size:
                15px !important;

            font-weight:
                900 !important;

            letter-spacing:
                0.05em;

            line-height:
                1.15;
        }}

        .sidebar-brand-subtitle {{
            margin-top:
                2px;

            color:
                #0284C7 !important;

            font-size:
                9px !important;

            font-weight:
                800 !important;

            letter-spacing:
                0.07em;

            line-height:
                1.3;
        }}


        /* ==================================================================
           SIDEBAR DIVIDER
           ================================================================== */

        .sidebar-divider {{
            height:
                1px;

            margin:
                0.25rem
                0.2rem
                0.35rem;

            background:
                linear-gradient(
                    90deg,
                    rgba(14, 165, 233, 0.35),
                    rgba(168, 85, 247, 0.15),
                    transparent
                );
        }}


        /* ==================================================================
           SIDEBAR SECTION LABELS (PERFECT ALIGNMENT & SPACING)
           ================================================================== */

        .sidebar-section-label {{
            margin-top:
                0.45rem !important;

            margin-bottom:
                0.15rem !important;

            margin-left:
                0.35rem !important;

            margin-right:
                0.35rem !important;

            padding:
                0 !important;

            color:
                #0369A1 !important;

            font-size:
                8.5px !important;

            font-weight:
                850 !important;

            letter-spacing:
                0.09em !important;

            line-height:
                1.25 !important;

            text-transform:
                uppercase !important;

            display:
                flex !important;

            align-items:
                center !important;

            gap:
                5px !important;

            position:
                relative !important;

            z-index:
                10 !important;
        }}

        .sidebar-section-label::before {{
            content:
                "" !important;

            display:
                inline-block !important;

            width:
                5px !important;

            height:
                5px !important;

            border-radius:
                50% !important;

            background:
                #38BDF8 !important;

            box-shadow:
                0 0 6px #0EA5E9 !important;

            flex-shrink:
                0 !important;
        }}

        .sidebar-section-label:first-of-type {{
            margin-top:
                0.1rem !important;
        }}


        /* ==================================================================
           CUSTOM PAGE-LINK NAVIGATION (HIGH CONTRAST & PERFECT FIT)
           ================================================================== */

        [data-testid="stSidebar"] .stPageLink {{
            width:
                100% !important;

            margin:
                0 !important;

            padding:
                0 !important;

            display:
                block !important;
        }}

        [data-testid="stSidebar"] .stPageLink > div {{
            width:
                100% !important;
        }}

        [data-testid="stSidebar"] .stPageLink a {{
            display:
                flex !important;

            align-items:
                center !important;

            width:
                100% !important;

            min-height:
                35px !important;

            height:
                35px !important;

            margin:
                0.1rem 0 !important;

            padding:
                0.35rem 0.8rem !important;

            border-radius:
                9px !important;

            background:
                rgba(255, 255, 255, 0.85) !important;

            backdrop-filter:
                blur(12px) !important;

            -webkit-backdrop-filter:
                blur(12px) !important;

            border:
                1px solid rgba(226, 232, 240, 0.95) !important;

            color:
                #0F172A !important;

            font-size:
                11.5px !important;

            font-weight:
                750 !important;

            letter-spacing:
                -0.01em !important;

            line-height:
                1.3 !important;

            text-decoration:
                none !important;

            box-shadow:
                0 1px 3px rgba(15, 23, 42, 0.02) !important;

            transition:
                all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;

            position:
                relative !important;

            z-index:
                5 !important;
        }}

        [data-testid="stSidebar"] .stPageLink a span,
        [data-testid="stSidebar"] .stPageLink a p {{
            color:
                #0F172A !important;

            font-weight:
                750 !important;

            font-size:
                11.5px !important;
        }}

        [data-testid="stSidebar"] .stPageLink a:hover {{
            background:
                #FFFFFF !important;

            color:
                #0284C7 !important;

            padding-left:
                1rem !important;

            border-color:
                rgba(14, 165, 233, 0.55) !important;

            box-shadow:
                0 4px 14px rgba(14, 165, 233, 0.14) !important;
        }}

        [data-testid="stSidebar"] .stPageLink a:hover span,
        [data-testid="stSidebar"] .stPageLink a:hover p {{
            color:
                #0284C7 !important;
        }}

        [data-testid="stSidebar"] .stPageLink a:focus-visible {{
            outline:
                2px solid #0EA5E9 !important;

            outline-offset:
                2px !important;
        }}

        /*
         * Active page - High-Impact Glowing Gradient
         */

        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] {{
            background:
                linear-gradient(
                    135deg,
                    #0EA5E9 0%,
                    #6366F1 100%
                ) !important;

            color:
                #FFFFFF !important;

            font-weight:
                850 !important;

            border:
                1px solid rgba(255, 255, 255, 0.45) !important;

            box-shadow:
                0 6px 18px rgba(14, 165, 233, 0.35),
                0 0 12px rgba(99, 102, 241, 0.25) !important;
        }}

        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] span,
        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] p {{
            color:
                #FFFFFF !important;

            font-weight:
                850 !important;
        }}

        [data-testid="stSidebar"] .stPageLink a > span:first-child {{
            width:
                22px !important;

            min-width:
                22px !important;

            display:
                inline-flex !important;

            align-items:
                center !important;

            justify-content:
                center !important;

            margin-right:
                0.45rem !important;

            font-size:
                13.5px !important;
        }}


        /* ==================================================================
           SIDEBAR FOOTER (FUTURISTIC FROSTED GLASS)
           ================================================================== */

        .sidebar-footer {{
            width:
                100% !important;

            max-width:
                100% !important;

            box-sizing:
                border-box !important;

            margin-top:
                0 !important;

            margin-bottom:
                0 !important;

            padding:
                0.55rem 0.85rem !important;

            border:
                1px solid rgba(186, 230, 253, 0.95);

            border-radius:
                12px;

            background:
                rgba(255, 255, 255, 0.92);

            backdrop-filter:
                blur(16px);

            -webkit-backdrop-filter:
                blur(16px);

            box-shadow:
                0 4px 16px rgba(14, 165, 233, 0.08);
        }}

        .sidebar-footer-status {{
            display:
                flex;

            align-items:
                center;

            gap:
                0.45rem;

            color:
                #0F172A;

            font-size:
                8.5px;

            font-weight:
                900;

            letter-spacing:
                0.08em;
        }}

        .sidebar-status-dot {{
            width:
                7px;

            height:
                7px;

            flex-shrink:
                0;

            border-radius:
                50%;

            background:
                #10B981;

            box-shadow:
                0 0 0 3px rgba(16, 185, 129, 0.25),
                0 0 8px rgba(16, 185, 129, 0.5);

            animation:
                status-pulse 2s infinite;
        }}

        @keyframes status-pulse {{
            0% {{
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5);
            }}
            70% {{
                transform: scale(1);
                box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
            }}
            100% {{
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }}
        }}

        .sidebar-footer-text {{
            margin-top:
                0.25rem;

            color:
                #0284C7;

            font-size:
                8px;

            font-weight:
                700;

            line-height:
                1.35;

            letter-spacing:
                0.03em;
        }}


        /* ==================================================================
           LEGACY STREAMLIT NAVIGATION
           ================================================================== */

        /*
         * Kept for compatibility if another part of the application uses
         * Streamlit's default navigation in the future.
         */

        [data-testid="stSidebarNav"] {{
            padding-top:
                0.25rem;
        }}

        [data-testid="stSidebarNav"] ul {{
            gap:
                0.2rem;
        }}

        [data-testid="stSidebarNav"] li {{
            margin-bottom:
                0.15rem;
        }}

        [data-testid="stSidebarNav"] a {{
            border-radius:
                9px;

            color:
                #94A3B8 !important;

            font-size:
                11px;

            font-weight:
                600;

            transition:
                background 0.15s ease,
                color 0.15s ease,
                transform 0.15s ease;
        }}

        [data-testid="stSidebarNav"] a:hover {{
            background:
                rgba(255, 255, 255, 0.05) !important;

            color:
                #F8FAFC !important;
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background:
                linear-gradient(
                    90deg,
                    rgba(37, 99, 235, 0.20),
                    rgba(124, 58, 237, 0.12)
                ) !important;

            color:
                #FFFFFF !important;

            box-shadow:
                inset 3px 0 0 {COLORS["primary"]};
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] span {{
            color:
                #FFFFFF !important;
        }}


        /* ==================================================================
           PAGE HEADER
           ================================================================== */

        .page-header {{
            position:
                relative;

            display:
                flex;

            align-items:
                flex-start;

            justify-content:
                space-between;

            gap:
                1.5rem;

            margin-bottom:
                2rem;

            padding:
                1.35rem 1.5rem;

            background:
                rgba(255, 255, 255, 0.88);

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                {SHADOWS["card"]};

            overflow:
                hidden;
        }}

        .page-header::before {{
            content:
                "";

            position:
                absolute;

            top:
                0;

            left:
                0;

            width:
                100%;

            height:
                3px;

            background:
                linear-gradient(
                    90deg,
                    {COLORS["primary"]},
                    {COLORS["secondary"]}
                );
        }}

        .page-header-content {{
            min-width:
                0;

            flex:
                1;
        }}

        .page-header-title {{
            color:
                {COLORS["text"]};

            font-size:
                25px;

            font-weight:
                800;

            line-height:
                1.2;

            letter-spacing:
                -0.025em;
        }}

        .page-header-description {{
            max-width:
                820px;

            margin-top:
                0.45rem;

            color:
                {COLORS["text_muted"]};

            font-size:
                12px;

            line-height:
                1.65;
        }}

        .page-header-status {{
            flex-shrink:
                0;

            padding-top:
                0.1rem;
        }}

        .status-badge {{
            display:
                inline-flex;

            align-items:
                center;

            gap:
                0.35rem;

            padding:
                0.38rem 0.7rem;

            border-radius:
                {RADIUS["pill"]};

            font-size:
                9px;

            font-weight:
                800;

            letter-spacing:
                0.05em;

            white-space:
                nowrap;
        }}

        .status-live {{
            color:
                {COLORS["success_dark"]};

            background:
                {COLORS["success_soft"]};

            border:
                1px solid {COLORS["success_light"]};
        }}

        .status-warning {{
            color:
                {COLORS["warning_dark"]};

            background:
                {COLORS["warning_soft"]};

            border:
                1px solid {COLORS["warning_light"]};
        }}

        .status-danger {{
            color:
                {COLORS["danger_dark"]};

            background:
                {COLORS["danger_soft"]};

            border:
                1px solid {COLORS["danger_light"]};
        }}

        .status-info {{
            color:
                {COLORS["info_dark"]};

            background:
                {COLORS["info_soft"]};

            border:
                1px solid {COLORS["info_light"]};
        }}


        /* ==================================================================
           SECTION HEADERS
           ================================================================== */

        .section-header {{
            position:
                relative;

            margin-top:
                1.75rem;

            margin-bottom:
                1rem;

            padding-left:
                0.9rem;
        }}

        .section-header::before {{
            content:
                "";

            position:
                absolute;

            top:
                3px;

            bottom:
                3px;

            left:
                0;

            width:
                3px;

            border-radius:
                3px;

            background:
                linear-gradient(
                    180deg,
                    {COLORS["primary"]},
                    {COLORS["secondary"]}
                );
        }}

        .section-title {{
            color:
                {COLORS["text"]};

            font-size:
                16px;

            font-weight:
                800;

            line-height:
                1.35;

            letter-spacing:
                -0.01em;
        }}

        .section-description {{
            margin-top:
                0.25rem;

            color:
                {COLORS["text_muted"]};

            font-size:
                10px;

            line-height:
                1.55;
        }}


        /* ==================================================================
           SUBSECTION HEADERS
           ================================================================== */

        .subsection-header {{
            margin-top:
                1.25rem;

            margin-bottom:
                0.75rem;
        }}

        .subsection-title {{
            color:
                {COLORS["text_secondary"]};

            font-size:
                12px;

            font-weight:
                750;

            line-height:
                1.4;
        }}

        .subsection-description {{
            margin-top:
                0.2rem;

            color:
                {COLORS["text_muted"]};

            font-size:
                9px;

            line-height:
                1.5;
        }}


        /* ==================================================================
           METRIC BADGES
           ================================================================== */

        .metric-badge {{
            display:
                inline-flex;

            align-items:
                center;

            padding:
                0.22rem 0.6rem;

            border-radius:
                {RADIUS["pill"]};

            font-size:
                9px;

            font-weight:
                800;

            letter-spacing:
                0.05em;

            line-height:
                1.2;

            text-transform:
                uppercase;

            white-space:
                nowrap;
        }}

        .metric-badge-positive {{
            background:
                #D1FAE5;

            color:
                #065F46;

            border:
                1px solid #A7F3D0;
        }}

        .metric-badge-negative {{
            background:
                #FEE2E2;

            color:
                #991B1B;

            border:
                1px solid #FECACA;
        }}

        .metric-badge-neutral {{
            background:
                #F1F5F9;

            color:
                #475569;

            border:
                1px solid #E2E8F0;
        }}

        .metric-badge-warning {{
            background:
                #FEF3C7;

            color:
                #92400E;

            border:
                1px solid #FDE68A;
        }}

        .metric-badge-info {{
            background:
                #E0F2FE;

            color:
                #075985;

            border:
                1px solid #BAE6FD;
        }}


        /* ==================================================================
           STATUS INDICATORS
           ================================================================== */

        .status-indicator {{
            display:
                inline-flex;

            align-items:
                center;

            gap:
                0.45rem;

            padding:
                0.3rem 0.7rem;

            border-radius:
                {RADIUS["pill"]};

            font-size:
                9px;

            font-weight:
                800;

            letter-spacing:
                0.06em;

            text-transform:
                uppercase;

            background:
                rgba(255, 255, 255, 0.85);

            border:
                1px solid rgba(226, 232, 240, 0.9);

            box-shadow:
                0 2px 6px rgba(15, 23, 42, 0.04);
        }}

        .status-indicator-dot {{
            width:
                7px;

            height:
                7px;

            border-radius:
                50%;

            display:
                inline-block;

            flex-shrink:
                0;
        }}

        .status-live .status-indicator-dot {{
            background:
                #10B981;

            box-shadow:
                0 0 0 3px rgba(16, 185, 129, 0.25);
        }}

        .status-healthy .status-indicator-dot {{
            background:
                #10B981;
        }}

        .status-warning .status-indicator-dot {{
            background:
                #F59E0B;

            box-shadow:
                0 0 0 3px rgba(245, 158, 11, 0.25);
        }}

        .status-error .status-indicator-dot {{
            background:
                #EF4444;

            box-shadow:
                0 0 0 3px rgba(239, 68, 68, 0.25);
        }}

        .status-processing .status-indicator-dot {{
            background:
                #0EA5E9;

            box-shadow:
                0 0 0 3px rgba(14, 165, 233, 0.25);
        }}

        .status-inactive .status-indicator-dot {{
            background:
                #94A3B8;
        }}


        /* ==================================================================
           EMPTY STATES (GLASSMORPHISM)
           ================================================================== */

        .empty-state {{
            padding:
                2.5rem 1.5rem;

            text-align:
                center;

            background:
                rgba(255, 255, 255, 0.85);

            backdrop-filter:
                blur(14px) saturate(180%);

            border:
                1px solid rgba(226, 232, 240, 0.85);

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                0 6px 20px -2px rgba(14, 165, 233, 0.05);

            margin:
                1rem 0;
        }}

        .empty-state-icon {{
            font-size:
                28px;

            margin-bottom:
                0.75rem;

            color:
                #0EA5E9;
        }}

        .empty-state-title {{
            color:
                #0F172A;

            font-size:
                14px;

            font-weight:
                800;

            margin-bottom:
                0.35rem;
        }}

        .empty-state-description {{
            color:
                #64748B;

            font-size:
                11px;

            max-width:
                480px;

            margin:
                0 auto;

            line-height:
                1.5;
        }}


        /* ==================================================================
           LOADING STATES & SKELETONS
           ================================================================== */

        @keyframes skeleton-shimmer {{
            0% {{
                background-position: -200% 0;
            }}
            100% {{
                background-position: 200% 0;
            }}
        }}

        .skeleton-card,
        .skeleton-chart-wrapper {{
            padding:
                1.25rem;

            background:
                rgba(255, 255, 255, 0.85);

            backdrop-filter:
                blur(14px);

            border:
                1px solid rgba(226, 232, 240, 0.85);

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                0 4px 16px rgba(14, 165, 233, 0.05);

            margin-bottom:
                1rem;
        }}

        .skeleton-line {{
            height:
                14px;

            border-radius:
                6px;

            margin-bottom:
                0.6rem;

            background:
                linear-gradient(
                    90deg,
                    #F1F5F9 25%,
                    #E2E8F0 50%,
                    #F1F5F9 75%
                );

            background-size:
                200% 100%;

            animation:
                skeleton-shimmer 1.8s infinite;
        }}

        .skeleton-value {{
            height:
                28px;
        }}

        .loading-state {{
            padding:
                2rem;

            text-align:
                center;

            color:
                #64748B;

            font-size:
                12px;

            font-weight:
                700;
        }}


        /* ==================================================================
           KPI CARDS
           ================================================================== */

        .kpi-card {{
            position:
                relative;

            min-height:
                125px;

            padding:
                1rem 1.15rem;

            background:
                rgba(255, 255, 255, 0.85);

            backdrop-filter:
                blur(14px) saturate(180%);

            -webkit-backdrop-filter:
                blur(14px) saturate(180%);

            border:
                1px solid rgba(226, 232, 240, 0.85);

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                0 6px 20px -2px rgba(14, 165, 233, 0.05),
                0 1px 3px 0 rgba(15, 23, 42, 0.03);

            overflow:
                hidden;

            transition:
                transform 0.22s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.22s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .kpi-card:hover {{
            transform:
                translateY(-2px);

            border-color:
                rgba(14, 165, 233, 0.40);

            box-shadow:
                0 12px 28px -4px rgba(14, 165, 233, 0.12),
                0 4px 8px -2px rgba(15, 23, 42, 0.04);
        }}

        .kpi-card::after {{
            content:
                "";

            position:
                absolute;

            left:
                0;

            right:
                0;

            bottom:
                0;

            height:
                3px;

            background:
                {COLORS["primary"]};
        }}

        .kpi-card.kpi-blue::after {{
            background:
                {COLORS["primary"]};
        }}

        .kpi-card.kpi-green::after {{
            background:
                {COLORS["success"]};
        }}

        .kpi-card.kpi-purple::after {{
            background:
                {COLORS["secondary"]};
        }}

        .kpi-card.kpi-amber::after {{
            background:
                {COLORS["warning"]};
        }}

        .kpi-card.kpi-red::after {{
            background:
                {COLORS["danger"]};
        }}

        .kpi-card-top {{
            position:
                relative;

            z-index:
                1;

            display:
                flex;

            align-items:
                flex-start;

            justify-content:
                space-between;

            gap:
                0.75rem;
        }}

        .kpi-card-content {{
            min-width:
                0;

            flex:
                1;
        }}

        .kpi-label {{
            color:
                {COLORS["text_muted"]};

            font-size:
                9px;

            font-weight:
                700;

            letter-spacing:
                0.055em;

            text-transform:
                uppercase;

            line-height:
                1.35;
        }}

        .kpi-value {{
            margin-top:
                0.35rem;

            color:
                {COLORS["text"]};

            font-size:
                25px;

            font-weight:
                800;

            line-height:
                1.15;

            letter-spacing:
                -0.03em;

            word-break:
                break-word;
        }}

        .kpi-footer {{
            margin-top:
                0.65rem;
        }}

        .kpi-positive,
        .kpi-negative,
        .kpi-neutral {{
            display:
                inline-flex;

            align-items:
                center;

            padding:
                0.25rem 0.5rem;

            border-radius:
                {RADIUS["pill"]};

            font-size:
                9px;

            font-weight:
                700;
        }}

        .kpi-positive {{
            color:
                {COLORS["success_dark"]};

            background:
                {COLORS["success_soft"]};
        }}

        .kpi-negative {{
            color:
                {COLORS["danger_dark"]};

            background:
                {COLORS["danger_soft"]};
        }}

        .kpi-neutral {{
            color:
                {COLORS["text_muted"]};

            background:
                {COLORS["surface_soft"]};
        }}

        .kpi-icon {{
            width:
                38px;

            height:
                38px;

            display:
                inline-flex;

            align-items:
                center;

            justify-content:
                center;

            flex-shrink:
                0;

            border-radius:
                11px;

            background:
                linear-gradient(
                    135deg,
                    {COLORS["primary_soft"]},
                    {COLORS["primary_light"]}
                );

            border:
                1px solid {COLORS["primary_light"]};

            color:
                {COLORS["primary"]};

            font-size:
                14px;

            font-weight:
                800;

            box-shadow:
                0 4px 10px rgba(37, 99, 235, 0.10);
        }}


        /* ==================================================================
        /* ==================================================================
           CHART & CONTENT CONTAINERS (GLASSMORPHISM ENTERPRISE PANELS)
           ================================================================== */

        .dashboard-panel,
        .chart-card,
        .dashboard-content-container,
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background:
                rgba(255, 255, 255, 0.94) !important;

            backdrop-filter:
                blur(18px) saturate(180%) !important;

            -webkit-backdrop-filter:
                blur(18px) saturate(180%) !important;

            border:
                1px solid rgba(226, 232, 240, 0.95) !important;

            border-radius:
                14px !important;

            padding:
                1.15rem 1.25rem !important;

            margin-bottom:
                1.15rem !important;

            box-shadow:
                0 4px 20px -2px rgba(14, 165, 233, 0.06),
                0 1px 3px 0 rgba(15, 23, 42, 0.03) !important;

            overflow:
                hidden !important;

            transition:
                all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .dashboard-panel:hover,
        .chart-card:hover,
        [data-testid="stVerticalBlockBorderWrapper"]:hover {{
            transform:
                translateY(-2px);

            border-color:
                rgba(14, 165, 233, 0.40) !important;

            box-shadow:
                0 12px 32px -4px rgba(14, 165, 233, 0.12),
                0 4px 10px -2px rgba(15, 23, 42, 0.04) !important;
        }}

        .dashboard-panel-header,
        .chart-card-header {{
            display:
                flex;

            flex-direction:
                column;

            gap:
                0.25rem;

            padding:
                0.2rem
                0.2rem
                0.75rem
                0.2rem;

            margin-bottom:
                0.85rem;

            border-bottom:
                1px solid rgba(226, 232, 240, 0.80);
        }}

        .dashboard-panel-title,
        .chart-card-title {{
            color:
                #0F172A;

            font-size:
                14.5px;

            font-weight:
                850;

            letter-spacing:
                -0.015em;

            line-height:
                1.25;
        }}

        .dashboard-panel-badge {{
            display:
                inline-flex;

            align-items:
                center;

            background:
                linear-gradient(
                    135deg,
                    rgba(14, 165, 233, 0.12) 0%,
                    rgba(99, 102, 241, 0.08) 100%
                );

            color:
                #0284C7;

            border:
                1px solid rgba(14, 165, 233, 0.28);

            border-radius:
                999px;

            padding:
                0.22rem 0.65rem;

            font-size:
                8px;

            font-weight:
                850;

            text-transform:
                uppercase;

            letter-spacing:
                0.08em;

            white-space:
                nowrap;
        }}

        .dashboard-panel-description,
        .chart-card-description {{
            color:
                #64748B;

            font-size:
                10.5px;

            line-height:
                1.55;

            margin-top:
                0.15rem;
        }}

        .dashboard-panel-footer {{
            margin-top:
                1rem;

            padding:
                0.65rem 0.9rem;

            background:
                linear-gradient(
                    135deg,
                    rgba(240, 249, 255, 0.95) 0%,
                    rgba(245, 243, 255, 0.85) 100%
                );

            border:
                1px solid rgba(186, 230, 253, 0.95);

            border-radius:
                11px;

            display:
                flex;

            align-items:
                center;

            gap:
                0.6rem;

            box-shadow:
                0 2px 8px rgba(14, 165, 233, 0.04);
        }}

        .dashboard-panel-footer-icon {{
            font-size:
                14px;

            flex-shrink:
                0;
        }}

        .dashboard-panel-footer-text {{
            color:
                #0369A1;

            font-size:
                10px;

            font-weight:
                750;

            line-height:
                1.45;
        }}

        /* ==================================================================
           INSIGHT & ALERT CARDS (GLASS EFFECT)
           ================================================================== */

        .insight-card {{
            position:
                relative;

            padding:
                1.15rem 1.25rem;

            background:
                rgba(255, 255, 255, 0.94);

            backdrop-filter:
                blur(16px) saturate(180%);

            -webkit-backdrop-filter:
                blur(16px) saturate(180%);

            border:
                1px solid rgba(226, 232, 240, 0.95);

            border-radius:
                14px;

            box-shadow:
                0 4px 20px -2px rgba(14, 165, 233, 0.05),
                0 1px 3px 0 rgba(15, 23, 42, 0.03);

            transition:
                transform 0.22s ease,
                border-color 0.22s ease,
                box-shadow 0.22s ease;
        }}

        .insight-card:hover {{
            transform:
                translateY(-2px);

            border-color:
                rgba(14, 165, 233, 0.35);

            box-shadow:
                0 12px 28px -4px rgba(14, 165, 233, 0.12);
        }}

        .insight-label {{
            display:
                inline-block;

            padding:
                0.22rem 0.65rem;

            border-radius:
                999px;

            font-size:
                8.5px;

            font-weight:
                850;

            letter-spacing:
                0.08em;

            text-transform:
                uppercase;

            margin-bottom:
                0.6rem;
        }}

        .insight-danger {{
            background:
                #FEE2E2;

            color:
                #DC2626;

            border:
                1px solid #FECACA;
        }}

        .insight-warning {{
            background:
                #FEF3C7;

            color:
                #D97706;

            border:
                1px solid #FDE68A;
        }}

        .insight-success {{
            background:
                #D1FAE5;

            color:
                #059669;

            border:
                1px solid #A7F3D0;
        }}

        .insight-info {{
            background:
                #E0F2FE;

            color:
                #0284C7;

            border:
                1px solid #BAE6FD;
        }}

        .insight-title {{
            color:
                #0F172A;

            font-size:
                13.5px;

            font-weight:
                850;

            line-height:
                1.35;

            margin-bottom:
                0.4rem;
        }}

        .insight-description {{
            color:
                #64748B;

            font-size:
                10.5px;

            line-height:
                1.55;
        }}


        /* ==================================================================
           DATA TABLES
           ================================================================== */

        .data-table-wrapper {{
            width:
                100%;

            overflow-x:
                auto;

            background:
                {COLORS["surface"]};

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                {SHADOWS["card"]};
        }}

        .data-table {{
            width:
                100%;

            border-collapse:
                collapse;

            font-size:
                10px;
        }}

        .data-table thead {{
            background:
                {COLORS["surface_soft"]};
        }}

        .data-table th {{
            padding:
                0.8rem 0.75rem;

            color:
                {COLORS["text_muted"]};

            font-size:
                9px;

            font-weight:
                800;

            letter-spacing:
                0.04em;

            text-align:
                left;

            text-transform:
                uppercase;

            border-bottom:
                1px solid {COLORS["border"]};
        }}

        .data-table td {{
            padding:
                0.75rem;

            color:
                {COLORS["text_secondary"]};

            border-bottom:
                1px solid {COLORS["border_light"]};

            vertical-align:
                middle;
        }}

        .data-table tbody tr {{
            transition:
                background 0.15s ease;
        }}

        .data-table tbody tr:hover {{
            background:
                {COLORS["primary_soft"]};
        }}

        .data-table tbody tr:last-child td {{
            border-bottom:
                none;
        }}

        .segment-name {{
            color:
                {COLORS["text"]};

            font-weight:
                700;
        }}

        .table-number {{
            color:
                {COLORS["text_secondary"]};

            font-variant-numeric:
                tabular-nums;

            text-align:
                right;
        }}

        .total-value {{
            color:
                {COLORS["primary"]};

            font-weight:
                750;
        }}

        .monetary {{
            font-variant-numeric:
                tabular-nums;
        }}


        /* ==================================================================
           BUTTONS
           ================================================================== */

        .stButton > button {{
            min-height:
                38px;

            padding:
                0.5rem 1rem;

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["md"]};

            background:
                {COLORS["surface"]};

            color:
                {COLORS["text_secondary"]};

            font-size:
                11px;

            font-weight:
                700;

            box-shadow:
                {SHADOWS["sm"]};

            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                color 0.15s ease,
                transform 0.15s ease;
        }}

        .stButton > button:hover {{
            border-color:
                {COLORS["primary"]};

            background:
                {COLORS["primary_soft"]};

            color:
                {COLORS["primary_dark"]};

            transform:
                translateY(-1px);
        }}

        .stButton > button:focus {{
            box-shadow:
                0 0 0 3px rgba(37, 99, 235, 0.14);
        }}


        /* ==================================================================
           SELECTBOX
           ================================================================== */

        [data-baseweb="select"] > div {{
            min-height:
                38px;

            background:
                {COLORS["surface"]} !important;

            border-color:
                {COLORS["border"]} !important;

            border-radius:
                {RADIUS["md"]} !important;

            color:
                {COLORS["text_secondary"]} !important;
        }}

        [data-baseweb="select"] span {{
            color:
                {COLORS["text_secondary"]} !important;

            font-size:
                11px;
        }}


        /* ==================================================================
           INPUTS
           ================================================================== */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input {{
            background:
                {COLORS["surface"]} !important;

            border:
                1px solid {COLORS["border"]} !important;

            border-radius:
                {RADIUS["md"]} !important;

            color:
                {COLORS["text"]} !important;

            font-size:
                11px;
        }}

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {{
            border-color:
                {COLORS["primary"]} !important;

            box-shadow:
                0 0 0 3px rgba(37, 99, 235, 0.10) !important;
        }}


        /* ==================================================================
           TABS
           ================================================================== */

        .stTabs [data-baseweb="tab-list"] {{
            gap:
                0.25rem;

            border-bottom:
                1px solid {COLORS["border"]};
        }}

        .stTabs [data-baseweb="tab"] {{
            padding:
                0.65rem 0.85rem;

            color:
                {COLORS["text_muted"]};

            font-size:
                10px;

            font-weight:
                700;
        }}

        .stTabs [aria-selected="true"] {{
            color:
                {COLORS["primary"]} !important;
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            background:
                {COLORS["primary"]} !important;
        }}


        /* ==================================================================
           ALERTS
           ================================================================== */

        [data-testid="stAlert"] {{
            border-radius:
                {RADIUS["md"]};

            border-width:
                1px;

            font-size:
                11px;
        }}


        /* ==================================================================
           STREAMLIT METRICS
           ================================================================== */

        [data-testid="stMetric"],
        [data-testid="stExpander"] {{
            padding:
                1rem 1.15rem;

            background:
                rgba(255, 255, 255, 0.94) !important;

            backdrop-filter:
                blur(16px) saturate(180%) !important;

            -webkit-backdrop-filter:
                blur(16px) saturate(180%) !important;

            border:
                1px solid rgba(226, 232, 240, 0.95) !important;

            border-radius:
                14px !important;

            box-shadow:
                0 4px 18px -2px rgba(14, 165, 233, 0.05) !important;
        }}

        [data-testid="stMetricLabel"] {{
            color:
                {COLORS["text_muted"]} !important;

            font-size:
                9px !important;
        }}

        [data-testid="stMetricValue"] {{
            color:
                {COLORS["text"]} !important;

            font-size:
                21px !important;

            font-weight:
                800 !important;
        }}


        /* ==================================================================
           DIVIDERS
           ================================================================== */

        hr {{
            margin:
                1.5rem 0;

            border:
                none;

            border-top:
                1px solid {COLORS["border"]};
        }}


        /* ==================================================================
           GLOBAL SCROLLBAR (MAIN CONTENT)
           ================================================================== */

        body::-webkit-scrollbar,
        [data-testid="stMain"]::-webkit-scrollbar,
        [data-testid="block-container"]::-webkit-scrollbar,
        ::-webkit-scrollbar {{
            width:
                7px;

            height:
                7px;
        }}

        ::-webkit-scrollbar-track {{
            background:
                {COLORS["surface_soft"]};
        }}

        ::-webkit-scrollbar-thumb {{
            background:
                #CBD5E1;

            border-radius:
                999px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background:
                #94A3B8;
        }}

        /* Completely suppress all scrollbars and sliders across sidebar elements */
        section[data-testid="stSidebar"]::-webkit-scrollbar,
        [data-testid="stSidebarContent"]::-webkit-scrollbar,
        [data-testid="stSidebarUserContent"]::-webkit-scrollbar,
        [data-testid="stSidebar"]::-webkit-scrollbar,
        [data-testid="stSidebar"] *::-webkit-scrollbar,
        .sidebar-header-region::-webkit-scrollbar,
        .sidebar-footer-region::-webkit-scrollbar {{
            display:
                none !important;

            width:
                0px !important;

            height:
                0px !important;

            background:
                transparent !important;
        }}

        section[data-testid="stSidebar"],
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarUserContent"],
        [data-testid="stSidebar"] * {{
            scrollbar-width:
                none !important;

            -ms-overflow-style:
                none !important;
        }}


        /* ==================================================================
           EXPANDER
           ================================================================== */

        [data-testid="stExpander"] {{
            background:
                {COLORS["surface"]};

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                {SHADOWS["sm"]};

            overflow:
                hidden;
        }}

        [data-testid="stExpander"] summary {{
            color:
                {COLORS["text"]};

            font-size:
                11px;

            font-weight:
                700;
        }}


        /* ==================================================================
           DATAFRAME
           ================================================================== */

        [data-testid="stDataFrame"] {{
            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            overflow:
                hidden;

            box-shadow:
                {SHADOWS["card"]};
        }}


        /* ==================================================================
           PLOTLY
           ================================================================== */

        .js-plotly-plot,
        .plot-container {{
            font-family:
                {FONT_FAMILY} !important;
        }}


        /* ==================================================================
           FILE UPLOADER
           ================================================================== */

        [data-testid="stFileUploader"] {{
            background:
                {COLORS["surface"]};

            border:
                1px dashed {COLORS["border_strong"]};

            border-radius:
                {RADIUS["lg"]};

            padding:
                0.5rem;
        }}


        /* ==================================================================
           CHECKBOX
           ================================================================== */

        [data-testid="stCheckbox"] label {{
            color:
                {COLORS["text_secondary"]};

            font-size:
                11px;
        }}


        /* ==================================================================
           SLIDER
           ================================================================== */

        [data-testid="stSlider"] {{
            padding-top:
                0.25rem;
        }}


        /* ==================================================================
           CAPTION
           ================================================================== */

        .stCaption {{
            color:
                {COLORS["text_muted"]} !important;

            font-size:
                9px !important;
        }}


        /* ==================================================================
           LINK BUTTONS
           ================================================================== */

        .stLinkButton > a {{
            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["md"]};

            background:
                {COLORS["surface"]};

            color:
                {COLORS["primary"]};

            font-size:
                10px;

            font-weight:
                700;
        }}

        .stLinkButton > a:hover {{
            border-color:
                {COLORS["primary"]};

            background:
                {COLORS["primary_soft"]};
        }}


        /* ==================================================================
           RESPONSIVE DESIGN
           ================================================================== */

        @media (max-width: 1100px) {{

            [data-testid="block-container"] {{
                padding-left:
                    1.25rem;

                padding-right:
                    1.25rem;
            }}

            .page-header-title {{
                font-size:
                    22px;
            }}

            .kpi-value {{
                font-size:
                    22px;
            }}
        }}


        @media (max-width: 768px) {{

            [data-testid="stSidebar"] {{
                min-width:
                    250px !important;

                max-width:
                    250px !important;
            }}

            [data-testid="block-container"] {{
                padding:
                    1rem
                    0.85rem
                    2rem;
            }}

            .page-header {{
                flex-direction:
                    column;

                padding:
                    1rem;
            }}

            .page-header-status {{
                padding-top:
                    0;
            }}

            .page-header-title {{
                font-size:
                    20px;
            }}

            .section-title {{
                font-size:
                    14px;
            }}

            .kpi-card {{
                min-height:
                    115px;

                padding:
                    0.85rem;
            }}

            .kpi-value {{
                font-size:
                    20px;
            }}
        }}


        @media (max-width: 480px) {{

            .page-header-title {{
                font-size:
                    18px;
            }}

            .page-header-description {{
                font-size:
                    10px;
            }}

            .kpi-label {{
                font-size:
                    8px;
            }}

            .kpi-value {{
                font-size:
                    18px;
            }}

            .kpi-icon {{
                width:
                    32px;

                height:
                    32px;

                border-radius:
                    9px;
            }}
        }}


        /* ==================================================================
           ACCESSIBILITY
           ================================================================== */

        :focus-visible {{
            outline:
                2px solid {COLORS["primary"]};

            outline-offset:
                2px;
        }}

        @media (prefers-reduced-motion: reduce) {{

            *,
            *::before,
            *::after {{
                scroll-behavior:
                    auto !important;

                transition:
                    none !important;

                animation:
                    none !important;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# PUBLIC API
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