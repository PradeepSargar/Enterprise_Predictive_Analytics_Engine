"""
Main Streamlit application entry point.

Responsibilities
----------------
- Configure the Streamlit application.
- Load the centralized dashboard design system.
- Register all dashboard pages.
- Provide a professional custom sidebar.
- Organize navigation into business sections.
- Run the selected dashboard page.

Page-level business logic does not belong here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


# ============================================================================
# PROJECT PATH CONFIGURATION
# ============================================================================

# app.py is located at:
#
#     2.0/
#     └── dashboards/
#         └── app.py
#
# Therefore, the project root is two levels above this file.
#
# Adding the project root to sys.path makes package imports such as:
#
#     from dashboards.styles.theme import inject_global_styles
#
# reliable when Streamlit starts the application.

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# PROJECT IMPORTS
# ============================================================================

from dashboards.styles.theme import inject_global_styles
from dashboards.utils.html import render_html
from dashboards.components.sidebar import render_sidebar


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Enterprise Predictive Analytics Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# GLOBAL DESIGN SYSTEM
# ============================================================================

# Load the centralized visual system before rendering the application.
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
# PAGE DEFINITIONS
# ============================================================================

PAGES_DIR = Path(__file__).resolve().parent / "pages"

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

executive_page = st.Page(
    str(PAGES_DIR / "01_Executive_Overview.py"),
    title="Executive Overview",
    icon=":material/dashboard:",
    default=True,
)


# ---------------------------------------------------------------------------
# Customer Intelligence
# ---------------------------------------------------------------------------

customer_analytics_page = st.Page(
    str(PAGES_DIR / "02_Customer_Analytics.py"),
    title="Customer Analytics",
    icon=":material/groups:",
)

customer_risk_page = st.Page(
    str(PAGES_DIR / "03_Customer_Risk.py"),
    title="Customer Risk",
    icon=":material/security:",
)

customer_segmentation_page = st.Page(
    str(PAGES_DIR / "07_Customer_Segmentation.py"),
    title="Customer Segmentation",
    icon=":material/account_tree:",
)


# ---------------------------------------------------------------------------
# Predictive Intelligence
# ---------------------------------------------------------------------------

revenue_forecast_page = st.Page(
    str(PAGES_DIR / "04_Revenue_Forecast.py"),
    title="Revenue Forecast",
    icon=":material/monitoring:",
)

model_performance_page = st.Page(
    str(PAGES_DIR / "05_Model_Performance.py"),
    title="Model Performance",
    icon=":material/model_training:",
)


# ---------------------------------------------------------------------------
# Data & Insights
# ---------------------------------------------------------------------------

data_explorer_page = st.Page(
    str(PAGES_DIR / "06_Data_Explorer.py"),
    title="Data Explorer",
    icon=":material/table_view:",
)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

about_page = st.Page(
    str(PAGES_DIR / "08_About.py"),
    title="About",
    icon=":material/info:",
)


# ============================================================================
# STREAMLIT NAVIGATION
# ============================================================================

# Streamlit's default navigation is hidden because we provide a custom
# professional sidebar below.
#
# The Page objects remain the single source of truth for routing.

navigation = st.navigation(
    {
        "Overview": [
            executive_page,
        ],

        "Customer Intelligence": [
            customer_analytics_page,
            customer_risk_page,
            customer_segmentation_page,
        ],

        "Predictive Intelligence": [
            revenue_forecast_page,
            model_performance_page,
        ],

        "Data & Insights": [
            data_explorer_page,
        ],

        "Application": [
            about_page,
        ],
    },
    position="hidden",
)

# ---------------------------------------------------------------------------
# Render Modular Sidebar Navigation
# ---------------------------------------------------------------------------

PAGES_MAP = {
    "executive_overview": executive_page,
    "customer_analytics": customer_analytics_page,
    "customer_risk": customer_risk_page,
    "customer_segmentation": customer_segmentation_page,
    "revenue_forecast": revenue_forecast_page,
    "model_performance": model_performance_page,
    "data_explorer": data_explorer_page,
    "about": about_page,
}

render_sidebar(
    current_page=navigation,
    pages=PAGES_MAP,
    brand_title="ENTERPRISE",
    brand_subtitle="Predictive Analytics Engine",
    status_text="Engine Online • v2.4",
)


# ============================================================================
# RUN SELECTED PAGE
# ============================================================================

navigation.run()