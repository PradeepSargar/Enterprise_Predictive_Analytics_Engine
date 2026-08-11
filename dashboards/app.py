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

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

executive_page = st.Page(
    "pages/01_Executive_Overview.py",
    title="Executive Overview",
    icon="📊",
)


# ---------------------------------------------------------------------------
# Customer Intelligence
# ---------------------------------------------------------------------------

customer_analytics_page = st.Page(
    "pages/02_Customer_Analytics.py",
    title="Customer Analytics",
    icon="👥",
)

customer_risk_page = st.Page(
    "pages/03_Customer_Risk.py",
    title="Customer Risk",
    icon="⚠️",
)

customer_segmentation_page = st.Page(
    "pages/07_Customer_Segmentation.py",
    title="Customer Segmentation",
    icon="🎯",
)


# ---------------------------------------------------------------------------
# Predictive Intelligence
# ---------------------------------------------------------------------------

revenue_forecast_page = st.Page(
    "pages/04_Revenue_Forecast.py",
    title="Revenue Forecast",
    icon="📈",
)

model_performance_page = st.Page(
    "pages/05_Model_Performance.py",
    title="Model Performance",
    icon="🤖",
)


# ---------------------------------------------------------------------------
# Data & Insights
# ---------------------------------------------------------------------------

data_explorer_page = st.Page(
    "pages/06_Data_Explorer.py",
    title="Data Explorer",
    icon="🔎",
)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

about_page = st.Page(
    "pages/08_About.py",
    title="About",
    icon="ℹ️",
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


# ============================================================================
# CUSTOM SIDEBAR
# ============================================================================

with st.sidebar:

    # ========================================================================
    # BRAND
    # ========================================================================

    render_html(
        '<div class="custom-sidebar-brand">'
        '<div class="sidebar-brand-mark">◈</div>'
        '<div class="sidebar-brand-text">'
        '<div class="sidebar-brand-title">ENTERPRISE</div>'
        '<div class="sidebar-brand-subtitle">PREDICTIVE ENGINE</div>'
        '</div>'
        '</div>'
    )


    # ========================================================================
    # DIVIDER
    # ========================================================================

    render_html('<div class="sidebar-divider"></div>')


    # ========================================================================
    # OVERVIEW
    # ========================================================================

    render_html('<div class="sidebar-section-label">Overview</div>')

    st.page_link(
        executive_page,
        label="Executive Overview",
        icon="📊",
    )


    # ========================================================================
    # CUSTOMER INTELLIGENCE
    # ========================================================================

    render_html('<div class="sidebar-section-label">Customer Intelligence</div>')

    st.page_link(
        customer_analytics_page,
        label="Customer Analytics",
        icon="👥",
    )

    st.page_link(
        customer_risk_page,
        label="Customer Risk",
        icon="⚠️",
    )

    st.page_link(
        customer_segmentation_page,
        label="Customer Segmentation",
        icon="🎯",
    )


    # ========================================================================
    # PREDICTIVE INTELLIGENCE
    # ========================================================================

    render_html('<div class="sidebar-section-label">Predictive Intelligence</div>')

    st.page_link(
        revenue_forecast_page,
        label="Revenue Forecast",
        icon="📈",
    )

    st.page_link(
        model_performance_page,
        label="Model Performance",
        icon="🤖",
    )


    # ========================================================================
    # DATA & INSIGHTS
    # ========================================================================

    render_html('<div class="sidebar-section-label">Data & Insights</div>')

    st.page_link(
        data_explorer_page,
        label="Data Explorer",
        icon="🔎",
    )


    # ========================================================================
    # APPLICATION
    # ========================================================================

    render_html('<div class="sidebar-section-label">Application</div>')

    st.page_link(
        about_page,
        label="About",
        icon="ℹ️",
    )


    # ========================================================================
    # SIDEBAR FOOTER
    # ========================================================================

    render_html(
        '<div class="sidebar-footer">'
        '<div class="sidebar-footer-status">'
        '<span class="sidebar-status-dot"></span>'
        'ANALYTICS ENGINE'
        '</div>'
        '<div class="sidebar-footer-text">'
        'Enterprise Predictive Analytics'
        '</div>'
        '</div>'
    )


# ============================================================================
# RUN SELECTED PAGE
# ============================================================================

navigation.run()