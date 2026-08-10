"""
Enterprise Dashboard Design System
-----------------------------------

Centralized visual system for the Enterprise Predictive Analytics Engine.

This module is responsible for:

- Global application styling
- Typography
- Sidebar navigation
- KPI cards
- Section headers
- Charts
- Tables
- Buttons
- Tabs
- Alerts
- Responsive layout behavior
- Accessibility-focused visual states

Design philosophy
-----------------
The dashboard uses a modern enterprise analytics aesthetic:

- Light analytical canvas
- Dark navigation sidebar
- White elevated surfaces
- Blue primary accent
- Violet secondary accent
- Subtle borders
- Minimal shadows
- Strong typography hierarchy
- Consistent spacing
- Data-first visual hierarchy

Architecture
------------
Pages and reusable components should not contain large blocks of CSS.

Instead:

    dashboards/
        styles/
            theme.py

provides the centralized visual system.

Usage
-----
Call ``inject_global_styles()`` once from the application entry point:

    from dashboards.styles.theme import inject_global_styles

    inject_global_styles()
"""

from __future__ import annotations

import streamlit as st


# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # ------------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------------
    "background": "#F4F7FB",
    "background_top": "#F8FAFC",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFC",
    "surface_soft": "#F1F5F9",

    # ------------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------------
    "sidebar": "#0B1220",
    "sidebar_surface": "#111827",
    "sidebar_hover": "#172033",
    "sidebar_active": "#172B4D",

    # ------------------------------------------------------------------------
    # Primary brand
    # ------------------------------------------------------------------------
    "primary": "#2563EB",
    "primary_dark": "#1D4ED8",
    "primary_light": "#DBEAFE",
    "primary_soft": "#EFF6FF",

    # ------------------------------------------------------------------------
    # Secondary brand
    # ------------------------------------------------------------------------
    "secondary": "#7C3AED",
    "secondary_dark": "#6D28D9",
    "secondary_light": "#EDE9FE",
    "secondary_soft": "#F5F3FF",

    # ------------------------------------------------------------------------
    # Semantic
    # ------------------------------------------------------------------------
    "success": "#059669",
    "success_dark": "#047857",
    "success_light": "#D1FAE5",
    "success_soft": "#ECFDF5",

    "warning": "#D97706",
    "warning_dark": "#B45309",
    "warning_light": "#FEF3C7",
    "warning_soft": "#FFFBEB",

    "danger": "#DC2626",
    "danger_dark": "#B91C1C",
    "danger_light": "#FEE2E2",
    "danger_soft": "#FEF2F2",

    "info": "#0891B2",
    "info_dark": "#0E7490",
    "info_light": "#CFFAFE",
    "info_soft": "#ECFEFF",

    # ------------------------------------------------------------------------
    # Text
    # ------------------------------------------------------------------------
    "text": "#0F172A",
    "text_secondary": "#334155",
    "text_muted": "#64748B",
    "text_light": "#94A3B8",
    "text_inverse": "#FFFFFF",

    # ------------------------------------------------------------------------
    # Borders
    # ------------------------------------------------------------------------
    "border": "#E2E8F0",
    "border_light": "#EEF2F7",
    "border_strong": "#CBD5E1",

    # ------------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------------
    "chart_blue": "#2563EB",
    "chart_purple": "#7C3AED",
    "chart_green": "#059669",
    "chart_amber": "#D97706",
    "chart_red": "#DC2626",
    "chart_cyan": "#0891B2",
    "chart_pink": "#DB2777",
    "chart_indigo": "#4F46E5",
    "chart_teal": "#0F766E",
    "chart_violet": "#9333EA",

    # ------------------------------------------------------------------------
    # Miscellaneous
    # ------------------------------------------------------------------------
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

    "sm": (
        "0 1px 2px rgba(15, 23, 42, 0.04)"
    ),

    "card": (
        "0 2px 8px rgba(15, 23, 42, 0.04)"
    ),

    "card_hover": (
        "0 8px 24px rgba(15, 23, 42, 0.08)"
    ),

    "md": (
        "0 8px 24px rgba(15, 23, 42, 0.08)"
    ),

    "lg": (
        "0 16px 40px rgba(15, 23, 42, 0.12)"
    ),
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

    This function should be called once from ``dashboards/app.py``
    before rendering the selected dashboard page.
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
            font-family: {FONT_FAMILY};
        }}

        .stApp {{
            background:
                linear-gradient(
                    180deg,
                    {COLORS["background_top"]} 0%,
                    {COLORS["background"]} 48%,
                    #F1F5F9 100%
                ) !important;

            color: {COLORS["text"]};
        }}


        /* ==================================================================
           MAIN CONTENT CANVAS
           
           Streamlit can inherit a dark application theme depending on the
           browser and Streamlit configuration. These explicit overrides
           guarantee that the analytical canvas remains light.
           ================================================================== */

        [data-testid="stAppViewContainer"] {{
            background:
                {COLORS["background"]} !important;
        }}

        [data-testid="stMain"] {{
            background:
                linear-gradient(
                    180deg,
                    {COLORS["background_top"]} 0%,
                    {COLORS["background"]} 48%,
                    #F1F5F9 100%
                ) !important;
        }}

        [data-testid="stMainBlockContainer"] {{
            background: transparent !important;
        }}

        [data-testid="block-container"] {{
            max-width: 1520px;

            background: transparent !important;

            padding-top: 2rem;
            padding-right: 2.25rem;
            padding-bottom: 3rem;
            padding-left: 2.25rem;
        }}


        /* ==================================================================
           MAIN CONTENT TEXT
           ================================================================== */

        .stApp p {{
            color: {COLORS["text_secondary"]};
        }}

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {{
            color: {COLORS["text"]};
        }}


        /* ==================================================================
           SIDEBAR
           ================================================================== */

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    {COLORS["sidebar"]} 0%,
                    #0F172A 100%
                ) !important;

            border-right:
                1px solid rgba(255, 255, 255, 0.06);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: transparent !important;
        }}

        [data-testid="stSidebar"] * {{
            box-sizing: border-box;
        }}

        [data-testid="stSidebar"] .stMarkdown {{
            color: #CBD5E1;
        }}

        [data-testid="stSidebar"] p {{
            color: #94A3B8;
        }}


        /* ==================================================================
           SIDEBAR BRAND
           ================================================================== */

        .sidebar-brand {{
            padding:
                0.35rem
                0.25rem
                1.5rem
                0.25rem;
        }}

        .sidebar-brand-row {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}

        .sidebar-brand-mark {{
            width: 42px;
            height: 42px;

            display: flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    {COLORS["primary"]},
                    {COLORS["secondary"]}
                );

            color: #FFFFFF;

            font-size: 13px;
            font-weight: 800;

            letter-spacing: 0.04em;

            box-shadow:
                0 8px 20px rgba(37, 99, 235, 0.25);
        }}

        .sidebar-brand-title {{
            color: #F8FAFC;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 0.08em;

            line-height: 1.3;
        }}

        .sidebar-brand-subtitle {{
            margin-top: 2px;

            color: #64748B;

            font-size: 9px;
            font-weight: 500;

            line-height: 1.4;
        }}


        /* ==================================================================
           SIDEBAR NAVIGATION
           ================================================================== */

        [data-testid="stSidebarNav"] {{
            padding-top: 0.25rem;
        }}

        [data-testid="stSidebarNav"] ul {{
            gap: 0.2rem;
        }}

        [data-testid="stSidebarNav"] li {{
            margin-bottom: 0.15rem;
        }}

        [data-testid="stSidebarNav"] a {{
            border-radius: 9px;

            color: #94A3B8 !important;

            font-size: 11px;
            font-weight: 600;

            transition:
                background 0.15s ease,
                color 0.15s ease,
                transform 0.15s ease;
        }}

        [data-testid="stSidebarNav"] a:hover {{
            background:
                rgba(255, 255, 255, 0.05) !important;

            color: #F8FAFC !important;
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background:
                linear-gradient(
                    90deg,
                    rgba(37, 99, 235, 0.20),
                    rgba(124, 58, 237, 0.12)
                ) !important;

            color: #FFFFFF !important;

            box-shadow:
                inset 3px 0 0 {COLORS["primary"]};
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] span {{
            color: #FFFFFF !important;
        }}


        /* ==================================================================
           PAGE HEADER
           ================================================================== */

        .page-header {{
            position: relative;

            display: flex;
            align-items: flex-start;
            justify-content: space-between;

            gap: 1.5rem;

            margin-bottom: 2rem;

            padding:
                1.35rem
                1.5rem;

            background:
                rgba(255, 255, 255, 0.88);

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                {SHADOWS["card"]};

            overflow: hidden;
        }}

        .page-header::before {{
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
                    {COLORS["secondary"]}
                );
        }}

        .page-header-content {{
            min-width: 0;
            flex: 1;
        }}

        .page-header-title {{
            color: {COLORS["text"]};

            font-size: 25px;
            font-weight: 800;

            line-height: 1.2;

            letter-spacing: -0.025em;
        }}

        .page-header-description {{
            max-width: 820px;

            margin-top: 0.45rem;

            color: {COLORS["text_muted"]};

            font-size: 12px;
            font-weight: 400;

            line-height: 1.65;
        }}

        .page-header-status {{
            flex-shrink: 0;

            padding-top: 0.1rem;
        }}

        .status-badge {{
            display: inline-flex;
            align-items: center;

            gap: 0.35rem;

            padding:
                0.38rem
                0.7rem;

            border-radius:
                {RADIUS["pill"]};

            font-size: 9px;
            font-weight: 800;

            letter-spacing: 0.05em;

            white-space: nowrap;
        }}

        .status-live {{
            color: {COLORS["success_dark"]};

            background:
                {COLORS["success_soft"]};

            border:
                1px solid {COLORS["success_light"]};
        }}

        .status-warning {{
            color: {COLORS["warning_dark"]};

            background:
                {COLORS["warning_soft"]};

            border:
                1px solid {COLORS["warning_light"]};
        }}

        .status-danger {{
            color: {COLORS["danger_dark"]};

            background:
                {COLORS["danger_soft"]};

            border:
                1px solid {COLORS["danger_light"]};
        }}

        .status-info {{
            color: {COLORS["info_dark"]};

            background:
                {COLORS["info_soft"]};

            border:
                1px solid {COLORS["info_light"]};
        }}


        /* ==================================================================
           SECTION HEADERS
           ================================================================== */

        .section-header {{
            position: relative;

            margin-top: 1.75rem;
            margin-bottom: 1rem;

            padding-left: 0.9rem;
        }}

        .section-header::before {{
            content: "";

            position: absolute;

            top: 3px;
            bottom: 3px;
            left: 0;

            width: 3px;

            border-radius: 3px;

            background:
                linear-gradient(
                    180deg,
                    {COLORS["primary"]},
                    {COLORS["secondary"]}
                );
        }}

        .section-title {{
            color: {COLORS["text"]};

            font-size: 16px;
            font-weight: 800;

            line-height: 1.35;

            letter-spacing: -0.01em;
        }}

        .section-description {{
            margin-top: 0.25rem;

            color: {COLORS["text_muted"]};

            font-size: 10px;

            line-height: 1.55;
        }}


        /* ==================================================================
           SUBSECTION HEADERS
           ================================================================== */

        .subsection-header {{
            margin-top: 1.25rem;
            margin-bottom: 0.75rem;
        }}

        .subsection-title {{
            color: {COLORS["text_secondary"]};

            font-size: 12px;
            font-weight: 750;

            line-height: 1.4;
        }}

        .subsection-description {{
            margin-top: 0.2rem;

            color: {COLORS["text_muted"]};

            font-size: 9px;

            line-height: 1.5;
        }}


        /* ==================================================================
           KPI CARDS
           ================================================================== */

        .kpi-card {{
            position: relative;

            min-height: 132px;

            padding:
                1rem
                1.1rem;

            background:
                {COLORS["surface"]};

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            box-shadow:
                {SHADOWS["card"]};

            overflow: hidden;

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
        }}

        .kpi-card:hover {{
            transform:
                translateY(-2px);

            border-color:
                #CBD5E1;

            box-shadow:
                {SHADOWS["card_hover"]};
        }}

        .kpi-card::after {{
            content: "";

            position: absolute;

            left: 0;
            right: 0;
            bottom: 0;

            height: 3px;

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
            position: relative;
            z-index: 1;

            display: flex;
            align-items: flex-start;
            justify-content: space-between;

            gap: 0.75rem;
        }}

        .kpi-card-content {{
            min-width: 0;
            flex: 1;
        }}

        .kpi-label {{
            color: {COLORS["text_muted"]};

            font-size: 9px;
            font-weight: 700;

            letter-spacing: 0.055em;

            text-transform: uppercase;

            line-height: 1.35;
        }}

        .kpi-value {{
            margin-top: 0.35rem;

            color: {COLORS["text"]};

            font-size: 25px;
            font-weight: 800;

            line-height: 1.15;

            letter-spacing: -0.03em;

            word-break: break-word;
        }}

        .kpi-footer {{
            margin-top: 0.65rem;
        }}

        .kpi-positive,
        .kpi-negative,
        .kpi-neutral {{
            display: inline-flex;
            align-items: center;

            padding:
                0.25rem
                0.5rem;

            border-radius:
                {RADIUS["pill"]};

            font-size: 9px;
            font-weight: 700;
        }}

        .kpi-positive {{
            color: {COLORS["success_dark"]};

            background:
                {COLORS["success_soft"]};
        }}

        .kpi-negative {{
            color: {COLORS["danger_dark"]};

            background:
                {COLORS["danger_soft"]};
        }}

        .kpi-neutral {{
            color: {COLORS["text_muted"]};

            background:
                {COLORS["surface_soft"]};
        }}

        .kpi-icon {{
            width: 38px;
            height: 38px;

            display: inline-flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 11px;

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

            font-size: 14px;
            font-weight: 800;

            box-shadow:
                0 4px 10px rgba(37, 99, 235, 0.10);
        }}


        /* ==================================================================
           CHART CONTAINERS
           ================================================================== */

        .chart-card {{
            background:
                {COLORS["surface"]};

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            padding:
                0.5rem;

            box-shadow:
                {SHADOWS["card"]};

            overflow: hidden;
        }}

        .chart-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 1rem;

            padding:
                0.8rem
                0.85rem
                0.35rem;
        }}

        .chart-card-title {{
            color: {COLORS["text"]};

            font-size: 12px;
            font-weight: 750;
        }}

        .chart-card-description {{
            margin-top: 0.15rem;

            color: {COLORS["text_muted"]};

            font-size: 9px;

            line-height: 1.45;
        }}


        /* ==================================================================
           DATA TABLES
           ================================================================== */

        .data-table-wrapper {{
            width: 100%;

            overflow-x: auto;

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
            width: 100%;

            border-collapse: collapse;

            font-size: 10px;
        }}

        .data-table thead {{
            background:
                {COLORS["surface_soft"]};
        }}

        .data-table th {{
            padding:
                0.8rem
                0.75rem;

            color:
                {COLORS["text_muted"]};

            font-size: 9px;
            font-weight: 800;

            letter-spacing: 0.04em;

            text-align: left;

            text-transform: uppercase;

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

            vertical-align: middle;
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
            border-bottom: none;
        }}

        .segment-name {{
            color:
                {COLORS["text"]};

            font-weight: 700;
        }}

        .table-number {{
            color:
                {COLORS["text_secondary"]};

            font-variant-numeric:
                tabular-nums;

            text-align: right;
        }}

        .total-value {{
            color:
                {COLORS["primary"]};

            font-weight: 750;
        }}

        .monetary {{
            font-variant-numeric:
                tabular-nums;
        }}


        /* ==================================================================
           BUTTONS
           ================================================================== */

        .stButton > button {{
            min-height: 38px;

            padding:
                0.5rem
                1rem;

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["md"]};

            background:
                {COLORS["surface"]};

            color:
                {COLORS["text_secondary"]};

            font-size: 11px;
            font-weight: 700;

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
            min-height: 38px;

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

            font-size: 11px;
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

            font-size: 11px;
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
            gap: 0.25rem;

            border-bottom:
                1px solid {COLORS["border"]};
        }}

        .stTabs [data-baseweb="tab"] {{
            padding:
                0.65rem
                0.85rem;

            color:
                {COLORS["text_muted"]};

            font-size: 10px;
            font-weight: 700;
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

            border-width: 1px;

            font-size: 11px;
        }}


        /* ==================================================================
           METRIC
           ================================================================== */

        [data-testid="stMetric"] {{
            padding:
                0.75rem;

            background:
                {COLORS["surface"]};

            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["md"]};

            box-shadow:
                {SHADOWS["sm"]};
        }}

        [data-testid="stMetricLabel"] {{
            color:
                {COLORS["text_muted"]} !important;

            font-size: 9px !important;
        }}

        [data-testid="stMetricValue"] {{
            color:
                {COLORS["text"]} !important;

            font-size: 21px !important;
            font-weight: 800 !important;
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
           SCROLLBAR
           ================================================================== */

        ::-webkit-scrollbar {{
            width: 7px;
            height: 7px;
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

            overflow: hidden;
        }}

        [data-testid="stExpander"] summary {{
            color:
                {COLORS["text"]};

            font-size: 11px;
            font-weight: 700;
        }}


        /* ==================================================================
           DATAFRAME
           ================================================================== */

        [data-testid="stDataFrame"] {{
            border:
                1px solid {COLORS["border"]};

            border-radius:
                {RADIUS["lg"]};

            overflow: hidden;

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

            font-size: 11px;
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

            font-size: 9px !important;
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

            font-size: 10px;
            font-weight: 700;
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
                padding-left: 1.25rem;
                padding-right: 1.25rem;
            }}

            .page-header-title {{
                font-size: 22px;
            }}

            .kpi-value {{
                font-size: 22px;
            }}
        }}


        @media (max-width: 768px) {{

            [data-testid="block-container"] {{
                padding:
                    1rem
                    0.85rem
                    2rem;
            }}

            .page-header {{
                flex-direction: column;

                padding:
                    1rem;
            }}

            .page-header-status {{
                padding-top: 0;
            }}

            .page-header-title {{
                font-size: 20px;
            }}

            .section-title {{
                font-size: 14px;
            }}

            .kpi-card {{
                min-height: 115px;

                padding:
                    0.85rem;
            }}

            .kpi-value {{
                font-size: 20px;
            }}
        }}


        @media (max-width: 480px) {{

            .page-header-title {{
                font-size: 18px;
            }}

            .page-header-description {{
                font-size: 10px;
            }}

            .kpi-label {{
                font-size: 8px;
            }}

            .kpi-value {{
                font-size: 18px;
            }}

            .kpi-icon {{
                width: 32px;
                height: 32px;

                border-radius: 9px;
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
                scroll-behavior: auto !important;

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