"""
Main Streamlit application entry point.

Responsibilities
----------------
1. Configure the Streamlit application.
2. Load the global design system.
3. Render the application shell.
4. Define centralized dashboard navigation.
5. Run the selected dashboard page.

Page-specific analytics remain inside dashboards/pages/.
"""

import streamlit as st

from dashboards.styles.theme import inject_global_styles
from dashboards.utils.html import render_html


# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Enterprise Predictive Analytics Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# GLOBAL DESIGN SYSTEM
# ============================================================================

# Load the centralized CSS design system before rendering the application.
inject_global_styles()


# ============================================================================
# APPLICATION NAVIGATION
# ============================================================================

# Navigation is organized according to the business purpose of each page.
#
# Only pages that currently exist are registered here.

pages = {

    # ------------------------------------------------------------------------
    # OVERVIEW
    # ------------------------------------------------------------------------

    "Overview": [
        st.Page(
            "dashboards/pages/01_Executive_Overview.py",
            title="Executive Overview",
            icon=":material/dashboard:",
            default=True,
        ),
    ],

    # ------------------------------------------------------------------------
    # CUSTOMER INTELLIGENCE
    # ------------------------------------------------------------------------

    "Customer Intelligence": [
        st.Page(
            "dashboards/pages/02_Customer_Analytics.py",
            title="Customer Analytics",
            icon=":material/groups:",
        ),
        st.Page(
            "dashboards/pages/03_Customer_Risk.py",
            title="Customer Risk",
            icon=":material/security:",
        ),
        st.Page(
            "dashboards/pages/07_Customer_Segmentation.py",
            title="Customer Segmentation",
            icon=":material/account_tree:",
        ),
    ],

    # ------------------------------------------------------------------------
    # PREDICTIVE INTELLIGENCE
    # ------------------------------------------------------------------------

    "Predictive Intelligence": [
        st.Page(
            "dashboards/pages/04_Revenue_Forecast.py",
            title="Revenue Forecast",
            icon=":material/monitoring:",
        ),
        st.Page(
            "dashboards/pages/05_Model_Performance.py",
            title="Model Performance",
            icon=":material/model_training:",
        ),
    ],

    # ------------------------------------------------------------------------
    # DATA & INSIGHTS
    # ------------------------------------------------------------------------

    "Data & Insights": [
        st.Page(
            "dashboards/pages/06_Data_Explorer.py",
            title="Data Explorer",
            icon=":material/table_view:",
        ),
    ],

    # ------------------------------------------------------------------------
    # APPLICATION
    # ------------------------------------------------------------------------

    "Application": [
        st.Page(
            "dashboards/pages/08_About.py",
            title="About & Architecture",
            icon=":material/info:",
        ),
    ],
}


# ============================================================================
# STREAMLIT NAVIGATION
# ============================================================================

# Streamlit renders the registered pages inside the sidebar.

page = st.navigation(
    pages,
    position="sidebar",
)


# ============================================================================
# SIDEBAR BRANDING
# ============================================================================

# Render the application identity using the centralized HTML renderer.
#
# The visual appearance of these elements is controlled by theme.py.

with st.sidebar:
    render_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark">
                ◈
            </div>

            <div class="sidebar-brand-title">
                ENTERPRISE ANALYTICS
            </div>

            <div class="sidebar-brand-subtitle">
                Predictive Intelligence Engine
            </div>
        </div>
        """
    )


# ============================================================================
# SIDEBAR FOOTER
# ============================================================================

# Display the application status and version information.

with st.sidebar:
    render_html(
        """
        <div class="sidebar-footer">

            <div class="sidebar-footer-status">
                <span class="sidebar-status-dot"></span>
                LIVE ANALYTICS
            </div>

            <div class="sidebar-footer-product">
                Enterprise Predictive Analytics Engine
            </div>

            <div class="sidebar-footer-version">
                Dashboard v2.0
            </div>

        </div>
        """
    )


# ============================================================================
# RUN SELECTED PAGE
# ============================================================================

# Execute the page selected by the user.

page.run()