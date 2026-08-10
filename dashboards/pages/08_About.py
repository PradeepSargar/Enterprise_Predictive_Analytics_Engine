"""
About
-----

Professional overview page for the
Enterprise Predictive Analytics Engine.

This page communicates:

- What the platform does
- Why the platform exists
- Core analytical capabilities
- Dashboard modules
- Analytical workflow
- Application architecture
- Technology stack
- Engineering principles

No business calculations or model training are performed here.
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
    title="Enterprise Predictive Analytics Engine",
    description=(
        "A unified analytics platform for customer intelligence, "
        "predictive modeling, forecasting, segmentation, and "
        "decision-oriented business analysis."
    ),
    status="PLATFORM OVERVIEW",
)


# ============================================================================
# HERO / VALUE PROPOSITION
# ============================================================================

render_html(
    """
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(
            135deg,
            #0F172A 0%,
            #172554 55%,
            #1E3A8A 100%
        );
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
    ">

        <div style="
            position: absolute;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: rgba(59, 130, 246, 0.12);
            top: -80px;
            right: 80px;
        "></div>

        <div style="
            position: absolute;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: rgba(124, 58, 237, 0.12);
            bottom: -65px;
            right: -20px;
        "></div>

        <div style="
            position: relative;
            z-index: 2;
            max-width: 820px;
        ">

            <div style="
                display: inline-block;
                padding: 0.3rem 0.65rem;
                border-radius: 999px;
                background: rgba(255,255,255,0.09);
                border: 1px solid rgba(255,255,255,0.14);
                color: #BFDBFE;
                font-size: 8px;
                font-weight: 800;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-bottom: 0.8rem;
            ">
                ANALYTICS PLATFORM
            </div>

            <div style="
                color: #FFFFFF;
                font-size: 27px;
                font-weight: 850;
                line-height: 1.2;
                margin-bottom: 0.65rem;
            ">
                Turning data into
                <span style="color: #93C5FD;">
                    decision-ready intelligence
                </span>
            </div>

            <div style="
                color: #CBD5E1;
                font-size: 11px;
                line-height: 1.75;
                max-width: 720px;
            ">
                The Enterprise Predictive Analytics Engine brings
                descriptive, diagnostic, predictive, and customer-focused
                analytics together in one structured dashboard experience.
            </div>

        </div>

    </div>
    """
)


# ============================================================================
# PLATFORM SNAPSHOT
# ============================================================================

snapshot_columns = st.columns(4, gap="medium")

snapshot_items = [
    ("07", "Analytics Modules", "Integrated dashboard views", "#2563EB"),
    ("04", "Analytical Layers", "From data to decisions", "#7C3AED"),
    ("01", "Unified Platform", "Single dashboard experience", "#059669"),
    ("∞", "Reusable Components", "Scalable UI architecture", "#D97706"),
]


for column, (
    value,
    label,
    description,
    accent,
) in zip(snapshot_columns, snapshot_items):

    with column:

        render_html(
            f"""
            <div class="chart-card">

                <div style="
                    padding: 1rem 1.05rem;
                    border-top: 3px solid {accent};
                ">

                    <div style="
                        color: {accent};
                        font-size: 22px;
                        font-weight: 850;
                        line-height: 1;
                        margin-bottom: 0.4rem;
                    ">
                        {value}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 10px;
                        font-weight: 800;
                        margin-bottom: 0.2rem;
                    ">
                        {label}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8px;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# WHAT THE PLATFORM DOES
# ============================================================================

section_header(
    title="What the Platform Does",
    description=(
        "The application connects multiple analytical perspectives "
        "into one decision-support environment."
    ),
)


capability_columns = st.columns(3, gap="medium")

capabilities = [
    (
        "01",
        "Understand",
        "Descriptive Analytics",
        "Explore customers, transactions, revenue, trends, "
        "and business performance.",
        "🔍",
        "#2563EB",
        "#EFF6FF",
    ),
    (
        "02",
        "Predict",
        "Predictive Analytics",
        "Use forecasting and machine learning workflows "
        "to estimate future outcomes and risk.",
        "🧠",
        "#7C3AED",
        "#F5F3FF",
    ),
    (
        "03",
        "Act",
        "Decision Intelligence",
        "Translate analytical results into interpretable "
        "insights and business-oriented actions.",
        "🎯",
        "#059669",
        "#ECFDF5",
    ),
]


for column, (
    number,
    title,
    subtitle,
    description,
    icon,
    accent,
    background,
) in zip(capability_columns, capabilities):

    with column:

        render_html(
            f"""
            <div class="chart-card" style="height: 100%;">

                <div style="
                    padding: 1.2rem;
                ">

                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 0.85rem;
                    ">

                        <div style="
                            width: 40px;
                            height: 40px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            border-radius: 11px;
                            background: {background};
                            font-size: 18px;
                        ">
                            {icon}
                        </div>

                        <div style="
                            color: #CBD5E1;
                            font-size: 9px;
                            font-weight: 800;
                        ">
                            {number}
                        </div>

                    </div>

                    <div style="
                        color: {accent};
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.08em;
                        text-transform: uppercase;
                        margin-bottom: 0.3rem;
                    ">
                        {subtitle}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 15px;
                        font-weight: 850;
                        margin-bottom: 0.45rem;
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
# ANALYTICAL WORKFLOW
# ============================================================================

section_header(
    title="From Data to Decisions",
    description=(
        "A structured analytical workflow connects raw information "
        "with business interpretation."
    ),
)


workflow = [
    (
        "01",
        "DATA",
        "Collect & Inspect",
        "Understand source structure, quality, and available fields.",
        "📥",
    ),
    (
        "02",
        "PREPARE",
        "Transform",
        "Clean, transform, and prepare analytical datasets.",
        "⚙️",
    ),
    (
        "03",
        "ANALYZE",
        "Model & Explore",
        "Apply analytics, segmentation, forecasting, and predictive models.",
        "📊",
    ),
    (
        "04",
        "DECIDE",
        "Interpret",
        "Present results through decision-oriented dashboards and insights.",
        "🎯",
    ),
]


for index, step in enumerate(workflow):

    number, label, title, description, icon = step

    column = st.columns([1, 0.08, 1, 0.08, 1, 0.08, 1])[index * 2]

    with column:

        render_html(
            f"""
            <div class="chart-card" style="
                min-height: 175px;
            ">

                <div style="padding: 1rem;">

                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 0.65rem;
                    ">

                        <div style="font-size: 21px;">
                            {icon}
                        </div>

                        <div style="
                            color: #94A3B8;
                            font-size: 8px;
                            font-weight: 800;
                        ">
                            {number}
                        </div>

                    </div>

                    <div style="
                        color: #2563EB;
                        font-size: 8px;
                        font-weight: 800;
                        letter-spacing: 0.08em;
                        margin-bottom: 0.25rem;
                    ">
                        {label}
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
                        font-size: 8.5px;
                        line-height: 1.6;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# DASHBOARD MODULES
# ============================================================================

section_header(
    title="Dashboard Modules",
    description=(
        "Each module addresses a specific analytical or business question."
    ),
)


modules = [
    (
        "01",
        "Executive Overview",
        "Business Performance",
        "High-level KPIs, trends, and executive-level performance indicators.",
        "📊",
        "#2563EB",
    ),
    (
        "02",
        "Customer Analytics",
        "Customer Intelligence",
        "Customer behavior, value, frequency, and purchasing analysis.",
        "👥",
        "#7C3AED",
    ),
    (
        "03",
        "Customer Risk",
        "Risk Intelligence",
        "Risk-oriented customer analysis and predictive insights.",
        "⚠️",
        "#DC2626",
    ),
    (
        "04",
        "Revenue Forecast",
        "Forecasting",
        "Forward-looking revenue trends and forecast analysis.",
        "📈",
        "#059669",
    ),
    (
        "05",
        "Model Performance",
        "Model Evaluation",
        "Compare and evaluate predictive model performance.",
        "🤖",
        "#D97706",
    ),
    (
        "06",
        "Data Explorer",
        "Data Intelligence",
        "Explore the underlying dataset and analytical dimensions.",
        "🔎",
        "#0891B2",
    ),
    (
        "07",
        "Customer Segmentation",
        "Segmentation",
        "Identify and understand distinct customer groups.",
        "🎯",
        "#9333EA",
    ),
]


module_columns = st.columns(2, gap="medium")

for index, (
    number,
    title,
    category,
    description,
    icon,
    accent,
) in enumerate(modules):

    with module_columns[index % 2]:

        render_html(
            f"""
            <div class="chart-card" style="
                margin-bottom: 0.8rem;
            ">

                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.85rem;
                    padding: 0.95rem 1rem;
                ">

                    <div style="
                        min-width: 40px;
                        width: 40px;
                        height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 10px;
                        background: {accent}12;
                        border: 1px solid {accent}25;
                        font-size: 17px;
                    ">
                        {icon}
                    </div>

                    <div style="
                        flex: 1;
                        min-width: 0;
                    ">

                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 0.45rem;
                            margin-bottom: 0.18rem;
                        ">

                            <div style="
                                color: #0F172A;
                                font-size: 11px;
                                font-weight: 850;
                            ">
                                {title}
                            </div>

                            <div style="
                                color: {accent};
                                font-size: 7px;
                                font-weight: 800;
                                text-transform: uppercase;
                                letter-spacing: 0.05em;
                            ">
                                {number}
                            </div>

                        </div>

                        <div style="
                            color: {accent};
                            font-size: 7.5px;
                            font-weight: 800;
                            text-transform: uppercase;
                            margin-bottom: 0.2rem;
                        ">
                            {category}
                        </div>

                        <div style="
                            color: #64748B;
                            font-size: 8.5px;
                            line-height: 1.5;
                        ">
                            {description}
                        </div>

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
        "The platform separates presentation, reusable UI, data logic, "
        "state management, and styling."
    ),
)


architecture_layers = [
    (
        "PRESENTATION",
        "Dashboard Pages",
        "Business-facing analytical views",
        "#2563EB",
    ),
    (
        "COMPONENTS",
        "Reusable UI",
        "KPI cards, headers, charts, exports",
        "#7C3AED",
    ),
    (
        "DATA",
        "Transformations",
        "Prepared datasets and analytical helpers",
        "#059669",
    ),
    (
        "STATE",
        "Session & Filters",
        "Shared filter and session management",
        "#D97706",
    ),
    (
        "STYLES",
        "Design System",
        "Centralized visual language and theme",
        "#DC2626",
    ),
]


for index, (
    layer,
    title,
    description,
    accent,
) in enumerate(architecture_layers):

    render_html(
        f"""
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 0.55rem;
        ">

            <div style="
                width: 115px;
                padding: 0.65rem 0.75rem;
                border-radius: 8px 0 0 8px;
                background: {accent};
                color: white;
                font-size: 8px;
                font-weight: 850;
                letter-spacing: 0.06em;
            ">
                {layer}
            </div>

            <div style="
                flex: 1;
                padding: 0.65rem 0.85rem;
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-left: none;
                border-radius: 0 8px 8px 0;
            ">

                <span style="
                    color: #0F172A;
                    font-size: 9px;
                    font-weight: 800;
                ">
                    {title}
                </span>

                <span style="
                    color: #94A3B8;
                    font-size: 8px;
                    margin-left: 0.5rem;
                ">
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
    title="Technology Stack",
    description=(
        "Core technologies supporting the analytical and application layers."
    ),
)


technologies = [
    ("🐍", "Python", "Core analytics and application logic."),
    ("🐼", "Pandas", "Data manipulation and analytical preparation."),
    ("🧠", "Scikit-learn", "Machine learning and predictive modeling."),
    ("⚡", "Streamlit", "Interactive dashboard application layer."),
]


technology_columns = st.columns(4, gap="medium")


for column, (
    icon,
    title,
    description,
) in zip(technology_columns, technologies):

    with column:

        render_html(
            f"""
            <div class="chart-card" style="height: 100%;">

                <div style="
                    padding: 1rem;
                    text-align: center;
                ">

                    <div style="
                        font-size: 22px;
                        margin-bottom: 0.55rem;
                    ">
                        {icon}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 11px;
                        font-weight: 850;
                        margin-bottom: 0.3rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8.5px;
                        line-height: 1.55;
                    ">
                        {description}
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
        "The application is designed around maintainability, consistency, "
        "and decision-oriented analytics."
    ),
)


principles = [
    (
        "01",
        "Separation of Concerns",
        "Pages focus on presentation while data, state, components, "
        "and styling remain independently organized.",
    ),
    (
        "02",
        "Reusable Components",
        "Shared visual elements are implemented once and reused "
        "across dashboard pages.",
    ),
    (
        "03",
        "Centralized Design",
        "A shared theme maintains consistent typography, spacing, "
        "colors, cards, and visual hierarchy.",
    ),
    (
        "04",
        "Decision-Oriented Analytics",
        "Visualizations focus on communicating patterns and insights "
        "rather than displaying charts for their own sake.",
    ),
]


principle_columns = st.columns(4, gap="medium")


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
                        font-weight: 850;
                        letter-spacing: 0.08em;
                        margin-bottom: 0.55rem;
                    ">
                        PRINCIPLE {number}
                    </div>

                    <div style="
                        color: #0F172A;
                        font-size: 11px;
                        font-weight: 850;
                        line-height: 1.3;
                        margin-bottom: 0.4rem;
                    ">
                        {title}
                    </div>

                    <div style="
                        color: #64748B;
                        font-size: 8.5px;
                        line-height: 1.6;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


# ============================================================================
# FINAL PROJECT STATEMENT
# ============================================================================

render_html(
    """
    <div style="
        margin-top: 1.8rem;
        padding: 1.35rem 1.5rem;
        border-radius: 14px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        text-align: center;
    ">

        <div style="
            color: #2563EB;
            font-size: 8px;
            font-weight: 850;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        ">
            ENTERPRISE PREDICTIVE ANALYTICS ENGINE
        </div>

        <div style="
            color: #0F172A;
            font-size: 15px;
            font-weight: 850;
            margin-bottom: 0.35rem;
        ">
            One platform. Multiple analytical perspectives.
        </div>

        <div style="
            color: #64748B;
            font-size: 9px;
            line-height: 1.6;
        ">
            Built to move from data exploration to predictive insight
            and business-oriented decision support.
        </div>

    </div>
    """
)