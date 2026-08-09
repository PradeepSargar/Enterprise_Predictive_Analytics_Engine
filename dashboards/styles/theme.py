"""
Enterprise Predictive Analytics Engine
---------------------------------------

Centralized visual design system for the Streamlit dashboard.

Keeping colors, typography, spacing, cards, buttons, navigation,
and common UI behavior in one place prevents individual pages
from developing inconsistent styling.
"""

import streamlit as st


# -------------------------------------------------------------------
# DESIGN TOKENS
# -------------------------------------------------------------------

# These values act as the single source of truth for the dashboard.
# If the visual identity needs to change later, we change it here
# instead of hunting through six different page files.

COLORS = {
    "background": "#F5F7FB",
    "surface": "#FFFFFF",
    "surface_soft": "#F8FAFC",
    "border": "#E5E7EB",
    "text_primary": "#111827",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",

    # Primary brand color.
    "primary": "#2563EB",
    "primary_dark": "#1D4ED8",
    "primary_soft": "#EFF6FF",

    # Semantic colors.
    "success": "#059669",
    "success_soft": "#ECFDF5",

    "warning": "#D97706",
    "warning_soft": "#FFFBEB",

    "danger": "#DC2626",
    "danger_soft": "#FEF2F2",

    "info": "#0891B2",
    "info_soft": "#ECFEFF",

    # Navigation.
    "sidebar": "#0B1220",
    "sidebar_surface": "#111827",
    "sidebar_text": "#CBD5E1",
    "sidebar_muted": "#64748B",
}


# -------------------------------------------------------------------
# TYPOGRAPHY
# -------------------------------------------------------------------

FONT_FAMILY = (
    "Inter, -apple-system, BlinkMacSystemFont, "
    '"Segoe UI", sans-serif'
)


# -------------------------------------------------------------------
# GLOBAL CSS
# -------------------------------------------------------------------

def inject_global_styles() -> None:
    """
    Inject the dashboard-wide CSS.

    This function should be called once from the application entry
    point so that every page receives the same visual foundation.
    """

    st.markdown(
        f"""
        <style>

        /* =========================================================
           GLOBAL APPLICATION
           ========================================================= */

        html, body, [class*="css"] {{
            font-family: {FONT_FAMILY};
        }}

        .stApp {{
            background: {COLORS["background"]};
            color: {COLORS["text_primary"]};
        }}

        .main .block-container {{
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }}


        /* =========================================================
           REMOVE DEFAULT STREAMLIT CHROME
           ========================================================= */

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header {{
            background: transparent !important;
        }}


        /* =========================================================
           SIDEBAR
           ========================================================= */

        section[data-testid="stSidebar"] {{
            background: {COLORS["sidebar"]};
            border-right: 1px solid rgba(255,255,255,0.06);
        }}

        section[data-testid="stSidebar"] > div {{
            background: {COLORS["sidebar"]};
        }}

        section[data-testid="stSidebar"] * {{
            color: {COLORS["sidebar_text"]};
        }}


        /* =========================================================
           SIDEBAR BRAND
           ========================================================= */

        .sidebar-brand {{
            padding: 0.5rem 0.4rem 1.8rem 0.4rem;
        }}

        .sidebar-brand-mark {{
            display: inline-flex;
            align-items: center;
            justify-content: center;

            width: 38px;
            height: 38px;

            border-radius: 11px;

            background: linear-gradient(
                135deg,
                {COLORS["primary"]},
                #7C3AED
            );

            color: white;
            font-size: 18px;
            font-weight: 800;

            box-shadow:
                0 8px 24px rgba(37, 99, 235, 0.25);
        }}

        .sidebar-brand-title {{
            margin-top: 0.75rem;

            color: #FFFFFF;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        .sidebar-brand-subtitle {{
            margin-top: 0.2rem;

            color: {COLORS["sidebar_muted"]};
            font-size: 11px;
            line-height: 1.5;
        }}


                /* =========================================================
           SIDEBAR NAVIGATION
           ========================================================= */

        /* Give the Streamlit navigation its own visual hierarchy. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
            padding: 0.25rem 0.65rem 1rem 0.65rem;
        }}

        /* Navigation groups such as:
           Overview
           Customer Intelligence
           Predictive Intelligence
           Data
        */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul {{
            gap: 0.2rem;
        }}

        /* Individual navigation items. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
            min-height: 42px;

            padding: 0.55rem 0.75rem;

            border-radius: 10px;

            color: {COLORS["sidebar_text"]} !important;

            font-size: 13px;
            font-weight: 550;

            transition:
                background 150ms ease,
                color 150ms ease,
                transform 150ms ease;
        }}

        /* Navigation hover state. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,0.055);

            color: #FFFFFF !important;

            transform: translateX(2px);
        }}

        /* Currently selected page. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(37, 99, 235, 0.18);

            color: #FFFFFF !important;

            font-weight: 650;

            box-shadow:
                inset 3px 0 0 {COLORS["primary"]},
                0 4px 14px rgba(0,0,0,0.10);
        }}

        /* Keep navigation icons aligned with their labels. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a svg {{
            width: 18px;
            height: 18px;

            margin-right: 0.55rem;
        }}

        /* Navigation group labels. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li > div {{
            color: {COLORS["sidebar_muted"]};
        }}

        /* Prevent excessive whitespace between navigation groups. */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] > ul {{
            padding-top: 0.35rem;
        }}


        /* =========================================================
           PAGE HEADER
           ========================================================= */

        .page-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;

            margin-bottom: 1.75rem;
        }}

        .page-header-title {{
            margin: 0;

            color: {COLORS["text_primary"]};

            font-size: 30px;
            font-weight: 750;

            letter-spacing: -0.035em;
            line-height: 1.15;
        }}

        .page-header-description {{
            margin-top: 0.55rem;

            color: {COLORS["text_secondary"]};

            font-size: 14px;
            line-height: 1.6;
        }}


        /* =========================================================
           KPI CARDS
           ========================================================= */

        .kpi-card {{
            position: relative;

            min-height: 142px;

            padding: 1.25rem;

            background: {COLORS["surface"]};

            border: 1px solid {COLORS["border"]};
            border-radius: 16px;

            box-shadow:
                0 1px 2px rgba(15, 23, 42, 0.03);

            transition:
                transform 160ms ease,
                box-shadow 160ms ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);

            box-shadow:
                0 10px 28px rgba(15, 23, 42, 0.07);
        }}

        .kpi-label {{
            color: {COLORS["text_secondary"]};

            font-size: 12px;
            font-weight: 600;

            text-transform: uppercase;
            letter-spacing: 0.055em;
        }}

        .kpi-value {{
            margin-top: 0.55rem;

            color: {COLORS["text_primary"]};

            font-size: 27px;
            font-weight: 750;

            letter-spacing: -0.035em;
        }}

        .kpi-footer {{
            display: flex;
            align-items: center;

            margin-top: 0.55rem;

            font-size: 12px;
        }}

        .kpi-positive {{
            color: {COLORS["success"]};
            font-weight: 650;
        }}

        .kpi-negative {{
            color: {COLORS["danger"]};
            font-weight: 650;
        }}

        .kpi-neutral {{
            color: {COLORS["text_muted"]};
        }}
        


        /* =========================================================
           SECTION HEADERS
           ========================================================= */

        .section-header {{
            margin-top: 1.5rem;
            margin-bottom: 0.9rem;
        }}

        .section-title {{
            color: {COLORS["text_primary"]};

            font-size: 17px;
            font-weight: 700;

            letter-spacing: -0.02em;
        }}

        .section-description {{
            margin-top: 0.2rem;

            color: {COLORS["text_secondary"]};

            font-size: 12px;
        }}


        /* =========================================================
           INSIGHT / ALERT CARDS
           ========================================================= */

        .insight-card {{
            padding: 1rem 1.1rem;

            border-radius: 14px;

            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
        }}

        .insight-label {{
            font-size: 10px;
            font-weight: 750;

            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .insight-title {{
            margin-top: 0.35rem;

            color: {COLORS["text_primary"]};

            font-size: 14px;
            font-weight: 700;
        }}

        .insight-description {{
            margin-top: 0.35rem;

            color: {COLORS["text_secondary"]};

            font-size: 12px;
            line-height: 1.55;
        }}

        /* Semantic insight colors.
           These must remain inside the CSS f-string. */

        .insight-danger {{
            color: {COLORS["danger"]};
        }}

        .insight-warning {{
            color: {COLORS["warning"]};
        }}

        .insight-success {{
            color: {COLORS["success"]};
        }}

        .insight-info {{
            color: {COLORS["info"]};
        }}


        /* =========================================================
           DATA TABLE
           ========================================================= */

        [data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid {COLORS["border"]};
        }}


        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button {{
            border-radius: 9px;

            border: 1px solid {COLORS["border"]};

            font-weight: 600;

            transition:
                border-color 150ms ease,
                box-shadow 150ms ease;
        }}

        .stButton > button:hover {{
            border-color: {COLORS["primary"]};

            box-shadow:
                0 4px 14px rgba(37, 99, 235, 0.12);
        }}


        /* =========================================================
           SELECTBOX / INPUTS
           ========================================================= */

        div[data-baseweb="select"] > div {{
            border-radius: 9px;
            border-color: {COLORS["border"]};
        }}

        div[data-baseweb="input"] > div {{
            border-radius: 9px;
            border-color: {COLORS["border"]};
        }}


        /* =========================================================
           CHART CONTAINERS
           ========================================================= */

        .chart-container {{
            padding: 0.4rem 0.4rem 0.2rem 0.4rem;

            background: {COLORS["surface"]};

            border: 1px solid {COLORS["border"]};
            border-radius: 16px;

            box-shadow:
                0 1px 2px rgba(15, 23, 42, 0.02);
        }}


        /* =========================================================
           STATUS BADGES
           ========================================================= */

        .status-badge {{
            display: inline-flex;

            align-items: center;

            padding: 0.28rem 0.6rem;

            border-radius: 999px;

            font-size: 10px;
            font-weight: 700;
        }}

        .status-live {{
            color: {COLORS["success"]};
            background: {COLORS["success_soft"]};
        }}

        .status-warning {{
            color: {COLORS["warning"]};
            background: {COLORS["warning_soft"]};
        }}

        .status-danger {{
            color: {COLORS["danger"]};
            background: {COLORS["danger_soft"]};
        }}


        /* =========================================================
           RESPONSIVE ADJUSTMENTS
           ========================================================= */

        @media (max-width: 900px) {{

            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .page-header-title {{
                font-size: 24px;
            }}

            .kpi-card {{
                min-height: 125px;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )