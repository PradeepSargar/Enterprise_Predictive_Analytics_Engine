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
    icon=":material/dashboard:",
)


# ---------------------------------------------------------------------------
# Customer Intelligence
# ---------------------------------------------------------------------------

customer_analytics_page = st.Page(
    "pages/02_Customer_Analytics.py",
    title="Customer Analytics",
    icon=":material/groups:",
)

customer_risk_page = st.Page(
    "pages/03_Customer_Risk.py",
    title="Customer Risk",
    icon=":material/security:",
)

customer_segmentation_page = st.Page(
    "pages/07_Customer_Segmentation.py",
    title="Customer Segmentation",
    icon=":material/account_tree:",
)


# ---------------------------------------------------------------------------
# Predictive Intelligence
# ---------------------------------------------------------------------------

revenue_forecast_page = st.Page(
    "pages/04_Revenue_Forecast.py",
    title="Revenue Forecast",
    icon=":material/monitoring:",
)

model_performance_page = st.Page(
    "pages/05_Model_Performance.py",
    title="Model Performance",
    icon=":material/model_training:",
)


# ---------------------------------------------------------------------------
# Data & Insights
# ---------------------------------------------------------------------------

data_explorer_page = st.Page(
    "pages/06_Data_Explorer.py",
    title="Data Explorer",
    icon=":material/table_view:",
)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

about_page = st.Page(
    "pages/08_About.py",
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
        '<div class="sidebar-brand-subtitle">Predictive Analytics</div>'
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

    render_html('<div class="sidebar-section-label">OVERVIEW</div>')

    st.page_link(
        executive_page,
        label="Executive Overview",
        icon=":material/dashboard:",
    )


    # ========================================================================
    # CUSTOMER INTELLIGENCE
    # ========================================================================

    render_html('<div class="sidebar-section-label">CUSTOMER INTELLIGENCE</div>')

    st.page_link(
        customer_analytics_page,
        label="Customer Analytics",
        icon=":material/groups:",
    )

    st.page_link(
        customer_risk_page,
        label="Customer Risk",
        icon=":material/security:",
    )

    st.page_link(
        customer_segmentation_page,
        label="Customer Segmentation",
        icon=":material/account_tree:",
    )


    # ========================================================================
    # PREDICTIVE INTELLIGENCE
    # ========================================================================

    render_html('<div class="sidebar-section-label">PREDICTIVE INTELLIGENCE</div>')

    st.page_link(
        revenue_forecast_page,
        label="Revenue Forecast",
        icon=":material/monitoring:",
    )

    st.page_link(
        model_performance_page,
        label="Model Performance",
        icon=":material/model_training:",
    )


    # ========================================================================
    # DATA & INSIGHTS
    # ========================================================================

    render_html('<div class="sidebar-section-label">DATA & INSIGHTS</div>')

    st.page_link(
        data_explorer_page,
        label="Data Explorer",
        icon=":material/table_view:",
    )


    # ========================================================================
    # APPLICATION
    # ========================================================================

    render_html('<div class="sidebar-section-label">APPLICATION</div>')

    st.page_link(
        about_page,
        label="About",
        icon=":material/info:",
    )


    # ========================================================================
    # SIDEBAR FOOTER / SYSTEM STATUS
    # ========================================================================

    render_html(
        '<div class="sidebar-footer">'
        '<div class="sidebar-footer-status">'
        '<span class="sidebar-status-dot"></span>'
        'ANALYTICS ENGINE'
        '</div>'
        '<div class="sidebar-footer-text">'
        'Enterprise Predictive Analytics Platform'
        '</div>'
        '</div>'
    )


# ============================================================================
# GLOBAL TOP APPLICATION NAVBAR / HEADER SECTION
# ============================================================================

render_html(
    """
    <header class="app-global-header" style="
        position: relative;
        width: 100%;
        margin-bottom: 1.25rem;
        padding: 0.85rem 1.4rem;
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 14px;
        box-shadow: 0 4px 20px -2px rgba(14, 165, 233, 0.08), 0 1px 3px rgba(15, 23, 42, 0.03);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        flex-wrap: wrap;
    ">
        <!-- Left Section: Project Topic Badge & Title -->
        <div style="display: flex; align-items: center; gap: 0.85rem; min-width: 260px;">
            <div style="
                width: 38px;
                height: 38px;
                border-radius: 10px;
                background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #FFFFFF;
                font-size: 18px;
                font-weight: 900;
                box-shadow: 0 4px 12px rgba(14, 165, 233, 0.35);
                flex-shrink: 0;
            ">
                ◈
            </div>
            <div>
                <div style="font-size: 8px; font-weight: 850; text-transform: uppercase; letter-spacing: 0.09em; color: #0284C7;">
                    Project Topic
                </div>
                <div style="font-size: 13.5px; font-weight: 900; color: #0F172A; letter-spacing: -0.01em;">
                    Enterprise Predictive Analytics Engine
                </div>
            </div>
        </div>

        <!-- Right Section: Submitted By & Registered Email ID Credentials -->
        <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
            <!-- Submitted By Card -->
            <div style="
                display: flex;
                align-items: center;
                gap: 0.6rem;
                padding: 0.45rem 0.85rem;
                border-radius: 10px;
                background: rgba(240, 253, 244, 0.85);
                border: 1px solid rgba(167, 243, 208, 0.95);
            ">
                <div style="
                    width: 26px;
                    height: 26px;
                    border-radius: 7px;
                    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                    color: #FFFFFF;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    flex-shrink: 0;
                ">👤</div>
                <div>
                    <div style="font-size: 7.5px; font-weight: 850; text-transform: uppercase; letter-spacing: 0.08em; color: #059669;">
                        Submitted By
                    </div>
                    <div style="font-size: 11.5px; font-weight: 850; color: #0F172A;">
                        Pradeep Bhagvat Sargar
                    </div>
                </div>
            </div>

            <!-- Registered Email Card -->
            <div style="
                display: flex;
                align-items: center;
                gap: 0.6rem;
                padding: 0.45rem 0.85rem;
                border-radius: 10px;
                background: rgba(245, 243, 255, 0.85);
                border: 1px solid rgba(221, 214, 254, 0.95);
            ">
                <div style="
                    width: 26px;
                    height: 26px;
                    border-radius: 7px;
                    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
                    color: #FFFFFF;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    flex-shrink: 0;
                ">✉️</div>
                <div>
                    <div style="font-size: 7.5px; font-weight: 850; text-transform: uppercase; letter-spacing: 0.08em; color: #7C3AED;">
                        Registered Email ID
                    </div>
                    <div style="font-size: 11.5px; font-weight: 850; color: #0F172A;">
                        pbsargar15@gmail.com
                    </div>
                </div>
            </div>

            <!-- Live Status Badge -->
            <div style="
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 0.45rem 0.75rem;
                border-radius: 10px;
                background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
                color: #FFFFFF;
                font-size: 8.5px;
                font-weight: 850;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                box-shadow: 0 4px 12px rgba(14, 165, 233, 0.28);
            ">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981; box-shadow: 0 0 6px #10B981;"></span>
                LIVE V2.4
            </div>
        </div>
    </header>
    """
)


# ============================================================================
# RUN SELECTED PAGE
# ============================================================================

navigation.run()