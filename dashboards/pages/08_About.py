"""
About Platform & System Architecture.
======================================
Enterprise Predictive Analytics Engine

This page provides an architectural blueprint, design principles,
technology stack details, and analytical capabilities of the Enterprise Predictive Analytics Engine.
"""

from __future__ import annotations

import streamlit as st

from dashboards.components.containers import panel
from dashboards.components.section_headers import page_header, section_header
from dashboards.utils.constants import PRIMARY_COLOR, SECONDARY_COLOR
from dashboards.utils.html import render_html

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Platform Architecture & Overview",
    description=(
        "Unified architecture blueprint, engineering standards, "
        "and analytical workflow powering the Enterprise Predictive Analytics Engine."
    ),
    status="PLATFORM OVERVIEW",
)

render_html(
    """
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 40%, #8B5CF6 100%);
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px -4px rgba(14, 165, 233, 0.25);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="position: relative; z-index: 2; max-width: 840px;">
            <div style="
                display: inline-block;
                padding: 0.25rem 0.6rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                font-size: 8.5px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            ">
                ENTERPRISE SYSTEM BLUEPRINT
            </div>
            <div style="font-size: 19px; font-weight: 900; line-height: 1.25; margin-bottom: 0.4rem; color: #FFFFFF;">
                End-to-End Predictive Analytics & Business Intelligence Engine
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.6; color: #F0F9FF;">
                Built on the Brazilian Olist e-commerce dataset (100k+ transactions), integrating
                Prophet time-series forecasting, Random Forest dissatisfaction risk classification,
                and K-Means RFM customer segmentation into an enterprise SaaS dashboard.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# PLATFORM TELEMETRY SNAPSHOT
# ============================================================================

snapshot_columns = st.columns(4, gap="medium")

snapshot_items = [
    ("08", "Analytics Modules", "Integrated dashboard pages", "#0EA5E9"),
    ("05", "Architectural Layers", "From raw data to decisions", "#8B5CF6"),
    ("96.5k", "Unique Orders Analyzed", "Verified transaction scale", "#10B981"),
    ("27", "Automated Pytest Suite", "100% verified test coverage", "#F59E0B"),
]

for column, (value, label, description, accent) in zip(snapshot_columns, snapshot_items):
    with column:
        render_html(
            f"""
            <div class="chart-card" style="border-top: 3px solid {accent}; padding: 1rem 1.1rem;">
                <div style="color: {accent}; font-size: 22px; font-weight: 900; line-height: 1; margin-bottom: 0.35rem;">
                    {value}
                </div>
                <div style="color: #0F172A; font-size: 11.5px; font-weight: 850; margin-bottom: 0.15rem;">
                    {label}
                </div>
                <div style="color: #64748B; font-size: 9px;">
                    {description}
                </div>
            </div>
            """
        )

# ============================================================================
# WHAT THE PLATFORM DELIVERS
# ============================================================================

section_header(
    title="Core Analytical Capabilities",
    description="Unified decision intelligence spanning descriptive, predictive, and prescriptive layers.",
)

capability_columns = st.columns(3, gap="medium")

capabilities = [
    (
        "01",
        "Descriptive & Diagnostic",
        "Executive & Customer Health",
        "Understand sales velocity, order cadence, logistics SLAs, and customer retention recency decay.",
        "📊",
        "#0EA5E9",
        "rgba(14, 165, 233, 0.12)",
    ),
    (
        "02",
        "Predictive & Forecasting",
        "Machine Learning Pipelines",
        "Multi-grain Prophet revenue forecasts with 90% confidence bands and Random Forest dissatisfaction risk scoring.",
        "🤖",
        "#8B5CF6",
        "rgba(139, 92, 246, 0.12)",
    ),
    (
        "03",
        "Prescriptive & Strategic",
        "Actionable Playbooks",
        "Proactive carrier SLA intervention, repeat buyer conversion triggers, and high-value customer nurturing.",
        "🎯",
        "#10B981",
        "rgba(16, 185, 129, 0.12)",
    ),
]

for column, (number, subtitle, title, description, icon, accent, background) in zip(capability_columns, capabilities):
    with column:
        render_html(
            f"""
            <div class="chart-card" style="height: 100%; padding: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 11px; background: {background}; font-size: 19px;">
                        {icon}
                    </div>
                    <div style="color: #94A3B8; font-size: 9px; font-weight: 800;">
                        {number}
                    </div>
                </div>
                <div style="color: {accent}; font-size: 8px; font-weight: 850; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.25rem;">
                    {subtitle}
                </div>
                <div style="color: #0F172A; font-size: 13.5px; font-weight: 900; margin-bottom: 0.35rem;">
                    {title}
                </div>
                <div style="color: #64748B; font-size: 9.5px; line-height: 1.6;">
                    {description}
                </div>
            </div>
            """
        )

# ============================================================================
# APPLICATION ARCHITECTURE
# ============================================================================

section_header(
    title="System Architecture & Modular Separation",
    description="Clean decoupled architecture separating UI presentation, state, transformations, and caching.",
)

architecture_layers = [
    ("PRESENTATION", "Streamlit Dashboard Pages (01 to 08)", "Independent analytical views with zero hardcoded business formulas.", "#0EA5E9"),
    ("COMPONENTS", "Reusable UI Design System", "KPI scorecard cards, section headers, Plotly SVG charts, glass panels, exports.", "#8B5CF6"),
    ("DATA LAYER", "Centralized Data Loader & Transformations", "Robust data validation, caching (@st.cache_data), and serialized ML pipelines.", "#10B981"),
    ("STATE & PARAMS", "Session State & Filter Handlers", "Centralized multi-grain parameters and user filter management.", "#F59E0B"),
    ("DESIGN SYSTEM", "CSS Tokens & Glassmorphism Theme", "Unified Sky Blue / Lavender palette, custom sidebar, and shimmer loading states.", "#6366F1"),
]

for layer, title, description, accent in architecture_layers:
    render_html(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 0.55rem;">
            <div style="width: 125px; padding: 0.65rem 0.8rem; border-radius: 9px 0 0 9px; background: {accent}; color: white; font-size: 8.5px; font-weight: 900; letter-spacing: 0.06em;">
                {layer}
            </div>
            <div style="flex: 1; padding: 0.65rem 0.95rem; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(226, 232, 240, 0.85); border-left: none; border-radius: 0 9px 9px 0;">
                <span style="color: #0F172A; font-size: 11px; font-weight: 850;">
                    {title}
                </span>
                <span style="color: #64748B; font-size: 9px; margin-left: 0.65rem;">
                    {description}
                </span>
            </div>
        </div>
        """
    )

# ============================================================================
# TECHNOLOGY STACK
# ============================================================================

section_header(
    title="Technology Stack & Standards",
    description="Production-grade analytical and visualization libraries.",
)

technologies = [
    ("🐍", "Python 3.13", "Core analytics, typed architecture, and execution engine."),
    ("⚡", "Streamlit 1.32+", "Reactive application shell and navigation runtime."),
    ("📊", "Plotly 5.24+", "Interactive charts with unified sky-blue / lavender palette."),
    ("🧠", "Scikit-Learn & Prophet", "Serialized classification models and multi-grain time-series forecasting."),
]

tech_columns = st.columns(4, gap="medium")

for column, (icon, title, description) in zip(tech_columns, technologies):
    with column:
        render_html(
            f"""
            <div class="chart-card" style="height: 100%; padding: 1.1rem; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 0.4rem;">
                    {icon}
                </div>
                <div style="color: #0F172A; font-size: 12px; font-weight: 850; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div style="color: #64748B; font-size: 9px; line-height: 1.55;">
                    {description}
                </div>
            </div>
            """
        )

# ============================================================================
# PROJECT SUBMISSION & AUTHORSHIP
# ============================================================================

section_header(
    title="Project Submission & Authorship",
    description="Official project registration and developer credentials.",
)

render_html(
    """
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 0.85rem;
        margin-bottom: 1.5rem;
    ">
        <div class="chart-card" style="padding: 1rem 1.15rem; display: flex; align-items: center; gap: 0.85rem;">
            <div style="
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(99, 102, 241, 0.15));
                border: 1px solid rgba(14, 165, 233, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 19px;
                flex-shrink: 0;
            ">📊</div>
            <div>
                <div style="font-size: 8.5px; font-weight: 850; text-transform: uppercase; letter-spacing: 0.08em; color: #0284C7;">Project Topic</div>
                <div style="font-size: 13px; font-weight: 850; color: #0F172A; margin-top: 1px;">Enterprise Predictive Analytics Engine</div>
            </div>
        </div>

        <div class="chart-card" style="padding: 1rem 1.15rem; display: flex; align-items: center; gap: 0.85rem;">
            <div style="
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15));
                border: 1px solid rgba(16, 185, 129, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 19px;
                flex-shrink: 0;
            ">👤</div>
            <div>
                <div style="font-size: 8.5px; font-weight: 850; text-transform: uppercase; letter-spacing: 0.08em; color: #059669;">Submitted By</div>
                <div style="font-size: 13px; font-weight: 850; color: #0F172A; margin-top: 1px;">Pradeep Bhagvat Sargar</div>
            </div>
        </div>

        <div class="chart-card" style="padding: 1rem 1.15rem; display: flex; align-items: center; gap: 0.85rem;">
            <div style="
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.15));
                border: 1px solid rgba(139, 92, 246, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 19px;
                flex-shrink: 0;
            ">✉️</div>
            <div>
                <div style="font-size: 8.5px; font-weight: 850; text-transform: uppercase; letter-spacing: 0.08em; color: #7C3AED;">Registered Email ID</div>
                <div style="font-size: 13px; font-weight: 850; color: #0F172A; margin-top: 1px;">pbsargar15@gmail.com</div>
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# FOOTER STATEMENT
# ============================================================================

render_html(
    """
    <div style="
        margin-top: 1.8rem;
        padding: 1.4rem 1.8rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(186, 230, 253, 0.9);
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.06);
        text-align: center;
    ">
        <div style="color: #0284C7; font-size: 8.5px; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.35rem;">
            ENTERPRISE PREDICTIVE ANALYTICS PLATFORM • v2.4
        </div>
        <div style="color: #0F172A; font-size: 15px; font-weight: 900; margin-bottom: 0.25rem;">
            Turning Raw E-Commerce Records into Actionable Executive Intelligence
        </div>
        <div style="color: #64748B; font-size: 9.5px; line-height: 1.6;">
            Designed and engineered as a modern, portfolio-ready business intelligence platform.
        </div>
    </div>
    """
)