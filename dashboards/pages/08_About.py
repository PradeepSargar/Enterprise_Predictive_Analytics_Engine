"""
About
-----

Professional project information page for the
Enterprise Predictive Analytics Engine.

This page provides:

- Platform overview
- Analytical capabilities
- Dashboard modules
- Analytical workflow
- Technology stack
- Application architecture
- Engineering principles

No business calculations or data processing are performed here.
"""

from __future__ import annotations

import streamlit as st

from dashboards.components.section_headers import (
    page_header,
    section_header,
)
from dashboards.utils.html import render_html


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="About the Analytics Platform",
    description=(
        "Enterprise Predictive Analytics Engine is an integrated analytics "
        "platform designed to transform transactional data into actionable "
        "business intelligence, customer insights, and predictive analysis."
    ),
    status="ANALYTICS PLATFORM",
)


# ============================================================================
# PLATFORM OVERVIEW
# ============================================================================

section_header(
    title="Platform Overview",
    description=(
        "A unified analytical environment combining descriptive, "
        "diagnostic, predictive, and customer-focused analytics."
    ),
)


render_html(
    """
    <div class="chart-card">
        <div style="padding: 1.35rem;">

            <div style="
                color: #2563EB;
                font-size: 9px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.45rem;
            ">
                ENTERPRISE ANALYTICS ENGINE
            </div>

            <div style="
                color: #0F172A;
                font-size: 20px;
                font-weight: 800;
                line-height: 1.3;
                margin-bottom: 0.65rem;
            ">
                From transactional data to decision-ready intelligence
            </div>

            <div style="
                color: #475569;
                font-size: 11px;
                line-height: 1.75;
                max-width: 950px;
            ">
                The platform brings multiple analytical workflows together
                inside a single dashboard experience. It combines customer
                analytics, segmentation, risk analysis, forecasting, model
                evaluation, and data exploration so that business questions
                can be investigated from multiple analytical perspectives.
            </div>

        </div>
    </div>
    """
)


# ============================================================================
# ANALYTICAL CAPABILITIES
# ============================================================================

section_header(
    title="Analytical Capabilities",
    description=(
        "Core analytical areas available throughout the platform."
    ),
)


capability_columns = st.columns(3, gap="medium")


capabilities = [
    (
        "👥",
        "Customer Intelligence",
        "Analyze customer behavior, purchasing patterns, "
        "customer value, frequency, recency, and retention "
        "characteristics.",
        "#2563EB",
        "#EFF6FF",
        "#DBEAFE",
    ),
    (
        "📈",
        "Predictive Analytics",
        "Apply predictive modeling and forecasting workflows "
        "to identify patterns, estimate future outcomes, and "
        "support forward-looking decisions.",
        "#7C3AED",
        "#F5F3FF",
        "#EDE9FE",
    ),
    (
        "🎯",
        "Decision Intelligence",
        "Convert analytical outputs into interpretable business "
        "insights through dashboards, comparisons, segmentation, "
        "and decision-oriented reporting.",
        "#059669",
        "#ECFDF5",
        "#D1FAE5",
    ),
]


for column, (
    icon,
    title,
    description,
    accent,
    background,
    border,
) in zip(capability_columns, capabilities):

    with column:

        render_html(
            f"""
            <div class="chart-card" style="height: 100%;">

                <div style="padding: 1.15rem;">

                    <div style="
                        width: 38px;
                        height: 38px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 10px;
                        background: {background};
                        border: 1px solid {border};
                        color: {accent};
                        font-size: 17px;
                        margin-bottom: 0.85rem;
                    ">
                        {icon}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 13px;
                        font-weight: 800;
                        margin-bottom: 0.4rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 10px;
                        line-height: 1.65;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# PLATFORM MODULES
# ============================================================================

section_header(
    title="Platform Modules",
    description=(
        "The dashboard is organized around distinct analytical workflows."
    ),
)


modules = [
    (
        "01",
        "Executive Overview",
        "High-level business KPIs and an executive view of overall performance.",
        "#2563EB",
    ),
    (
        "02",
        "Customer Analytics",
        "Customer-level behavioral and value-oriented analysis.",
        "#7C3AED",
    ),
    (
        "03",
        "Customer Risk",
        "Customer risk analysis and predictive risk-oriented insights.",
        "#DC2626",
    ),
    (
        "04",
        "Revenue Forecast",
        "Forward-looking revenue analysis and forecasting.",
        "#059669",
    ),
    (
        "05",
        "Model Performance",
        "Comparison and evaluation of predictive model performance.",
        "#D97706",
    ),
    (
        "06",
        "Data Explorer",
        "Interactive exploration of underlying analytical data.",
        "#0891B2",
    ),
    (
        "07",
        "Customer Segmentation",
        "Behavioral segmentation for identifying distinct customer groups.",
        "#9333EA",
    ),
]


module_columns = st.columns(2, gap="medium")


for index, (
    number,
    title,
    description,
    accent,
) in enumerate(modules):

    with module_columns[index % 2]:

        render_html(
            f"""
            <div class="chart-card" style="margin-bottom: 0.8rem;">

                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 0.9rem;
                    padding: 1rem 1.05rem;
                ">

                    <div style="
                        min-width: 34px;
                        width: 34px;
                        height: 34px;

                        display: flex;
                        align-items: center;
                        justify-content: center;

                        border-radius: 9px;

                        background: {accent}12;
                        color: {accent};

                        font-size: 9px;
                        font-weight: 800;

                        border: 1px solid {accent}25;
                    ">
                        {number}
                    </div>

                    <div style="flex: 1;">

                        <div style="
                            color: #0F172A;
                            font-size: 11px;
                            font-weight: 800;
                            margin-bottom: 0.25rem;
                        ">
                            {title}
                        </div>

                        <div style="
                            color: #64748B;
                            font-size: 9px;
                            line-height: 1.55;
                        ">
                            {description}
                        </div>

                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# ANALYTICAL WORKFLOW
# ============================================================================

section_header(
    title="Analytical Workflow",
    description=(
        "The platform follows a structured progression from raw data "
        "to analytical interpretation."
    ),
)


workflow_columns = st.columns(4, gap="small")


workflow_steps = [
    ("01", "Data", "Load and inspect source data.", "📥"),
    ("02", "Transform", "Prepare analytical features and datasets.", "⚙️"),
    ("03", "Analyze", "Apply statistical and predictive techniques.", "📊"),
    ("04", "Decide", "Present insights through business-focused dashboards.", "🎯"),
]


for column, (
    number,
    title,
    description,
    icon,
) in zip(workflow_columns, workflow_steps):

    with column:

        render_html(
            f"""
            <div class="chart-card" style="
                min-height: 150px;
                text-align: center;
            ">

                <div style="padding: 1rem 0.75rem;">

                    <div style="
                        font-size: 20px;
                        margin-bottom: 0.45rem;
                    ">
                        {icon}
                    </div>

                    <div style="
                        color: #2563EB;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.06em;
                        margin-bottom: 0.25rem;
                    ">
                        STEP {number}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 11px;
                        font-weight: 800;
                        margin-bottom: 0.3rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 9px;
                        line-height: 1.5;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# TECHNOLOGY STACK
# ============================================================================

section_header(
    title="Technology Stack",
    description=(
        "Core technologies used across the analytics and dashboard layers."
    ),
)


technology_columns = st.columns(4, gap="medium")


technologies = [
    (
        "🐍",
        "Python",
        "Core programming language for analytics and application logic.",
    ),
    (
        "📦",
        "Pandas",
        "Data manipulation, transformation, and analytical preparation.",
    ),
    (
        "🧠",
        "Scikit-learn",
        "Machine learning workflows and predictive modeling.",
    ),
    (
        "⚡",
        "Streamlit",
        "Interactive dashboard and application interface.",
    ),
]


for column, (
    icon,
    title,
    description,
) in zip(technology_columns, technologies):

    with column:

        render_html(
            f"""
            <div class="chart-card" style="min-height: 145px;">

                <div style="padding: 1rem;">

                    <div style="
                        font-size: 20px;
                        margin-bottom: 0.55rem;
                    ">
                        {icon}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 11px;
                        font-weight: 800;
                        margin-bottom: 0.3rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 9px;
                        line-height: 1.55;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# APPLICATION ARCHITECTURE
# ============================================================================

section_header(
    title="Application Architecture",
    description=(
        "The dashboard separates presentation, reusable components, "
        "data transformations, state, and styling."
    ),
)


render_html(
    """
    <div class="chart-card">

        <div style="
            padding: 1.15rem 1.25rem;
        ">

            <div style="
                display: grid;
                grid-template-columns:
                    repeat(5, minmax(0, 1fr));
                gap: 0.65rem;
            ">

                <div style="
                    padding: 0.85rem;
                    background: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                ">
                    <div style="
                        color: #2563EB;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.05em;
                    ">
                        PRESENTATION
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 10px;
                        font-weight: 750;
                        margin-top: 0.3rem;
                    ">
                        Pages
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8px;
                        margin-top: 0.25rem;
                    ">
                        Dashboard views
                    </div>
                </div>


                <div style="
                    padding: 0.85rem;
                    background: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                ">
                    <div style="
                        color: #7C3AED;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.05em;
                    ">
                        COMPONENTS
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 10px;
                        font-weight: 750;
                        margin-top: 0.3rem;
                    ">
                        UI Layer
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8px;
                        margin-top: 0.25rem;
                    ">
                        Reusable visuals
                    </div>
                </div>


                <div style="
                    padding: 0.85rem;
                    background: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                ">
                    <div style="
                        color: #059669;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.05em;
                    ">
                        DATA
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 10px;
                        font-weight: 750;
                        margin-top: 0.3rem;
                    ">
                        Transformations
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8px;
                        margin-top: 0.25rem;
                    ">
                        Analytical datasets
                    </div>
                </div>


                <div style="
                    padding: 0.85rem;
                    background: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                ">
                    <div style="
                        color: #D97706;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.05em;
                    ">
                        STATE
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 10px;
                        font-weight: 750;
                        margin-top: 0.3rem;
                    ">
                        Filters
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8px;
                        margin-top: 0.25rem;
                    ">
                        Session state
                    </div>
                </div>


                <div style="
                    padding: 0.85rem;
                    background: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                ">
                    <div style="
                        color: #DC2626;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.05em;
                    ">
                        STYLES
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 10px;
                        font-weight: 750;
                        margin-top: 0.3rem;
                    ">
                        Design System
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8px;
                        margin-top: 0.25rem;
                    ">
                        Centralized theme
                    </div>
                </div>

            </div>

        </div>

    </div>
    """
)


# ============================================================================
# ENGINEERING PRINCIPLES
# ============================================================================

section_header(
    title="Engineering Principles",
    description=(
        "Design and development principles followed throughout "
        "the dashboard application."
    ),
)


principle_columns = st.columns(3, gap="medium")


principles = [
    (
        "01",
        "Separation of Concerns",
        "Pages focus on presentation while reusable components, "
        "data transformations, state, and styling remain separated.",
    ),
    (
        "02",
        "Reusable Components",
        "Common dashboard elements are implemented once and reused "
        "across analytical pages for visual consistency.",
    ),
    (
        "03",
        "Decision-Oriented Design",
        "Visualizations are intended to communicate business patterns "
        "rather than simply display raw data.",
    ),
]


for column, (
    number,
    title,
    description,
) in zip(principle_columns, principles):

    with column:

        render_html(
            f"""
            <div class="chart-card" style="height: 100%;">

                <div style="padding: 1rem;">

                    <div style="
                        color: #94A3B8;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.08em;
                        margin-bottom: 0.5rem;
                    ">
                        PRINCIPLE {number}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 12px;
                        font-weight: 800;
                        margin-bottom: 0.35rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 9px;
                        line-height: 1.65;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# FOOTER
# ============================================================================

render_html(
    """
    <div style="
        margin-top: 2.25rem;
        padding: 1rem 0;
        border-top: 1px solid #E2E8F0;
        text-align: center;
    ">

        <div style="
            color: #0F172A;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.04em;
        ">
            ENTERPRISE PREDICTIVE ANALYTICS ENGINE
        </div>

        <div style="
            margin-top: 0.25rem;
            color: #94A3B8;
            font-size: 8px;
        ">
            Integrated analytics • Predictive intelligence • Decision support
        </div>

    </div>
    """
)