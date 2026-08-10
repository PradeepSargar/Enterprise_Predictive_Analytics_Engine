"""
Enterprise Predictive Analytics Engine
---------------------------------------

Main Streamlit application entry point.

Responsibilities
----------------
- Configure the Streamlit application.
- Load the centralized dashboard theme.
- Register dashboard pages.
- Organize navigation into business sections.
- Run the selected page.

Page-level business logic does not belong here.
"""

from __future__ import annotations

import streamlit as st

from dashboards.styles.theme import inject_global_styles


# ============================================================================
# PAGE CONFIGURATION
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

# Load the centralized visual system before any dashboard page is rendered.
#
# This controls:
# - Application background
# - Typography
# - Sidebar
# - Navigation
# - KPI cards
# - Section headers
# - Charts
# - Tables
# - Buttons
# - Responsive behavior

inject_global_styles()


# ============================================================================
# APPLICATION NAVIGATION
# ============================================================================

pages = {
    # ------------------------------------------------------------------------
    # Overview
    # ------------------------------------------------------------------------
    "Overview": [
        st.Page(
            "dashboards/pages/01_Executive_Overview.py",
            title="Executive Overview",
            icon="▦",
        ),
    ],

    # ------------------------------------------------------------------------
    # Customer Intelligence
    # ------------------------------------------------------------------------
    "Customer Intelligence": [
        st.Page(
            "dashboards/pages/02_Customer_Analytics.py",
            title="Customer Analytics",
            icon="♟",
        ),

        st.Page(
            "dashboards/pages/03_Customer_Risk.py",
            title="Customer Risk",
            icon="◈",
        ),

        st.Page(
            "dashboards/pages/07_Customer_Segmentation.py",
            title="Customer Segmentation",
            icon="⌘",
        ),
    ],

    # ------------------------------------------------------------------------
    # Predictive Intelligence
    # ------------------------------------------------------------------------
    "Predictive Intelligence": [
        st.Page(
            "dashboards/pages/04_Revenue_Forecast.py",
            title="Revenue Forecast",
            icon="⌁",
        ),

        st.Page(
            "dashboards/pages/05_Model_Performance.py",
            title="Model Performance",
            icon="◉",
        ),
    ],

    # ------------------------------------------------------------------------
    # Data & Insights
    # ------------------------------------------------------------------------
    "Data & Insights": [
        st.Page(
            "dashboards/pages/06_Data_Explorer.py",
            title="Data Explorer",
            icon="▤",
        ),
    ],
}


# ============================================================================
# NAVIGATION
# ============================================================================

# Streamlit renders the grouped navigation in the sidebar.
page = st.navigation(
    pages,
    position="sidebar",
)


# ============================================================================
# RUN SELECTED PAGE
# ============================================================================

page.run()