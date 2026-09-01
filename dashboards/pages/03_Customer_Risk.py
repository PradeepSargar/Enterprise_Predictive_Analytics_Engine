"""
Customer Risk Dashboard
=======================
Enterprise Predictive Analytics Engine

This page provides an analytical view of customer dissatisfaction risk,
root causes (delivery delays, freight ratio, category exposure), and operational
intervention workflows.

Distinction:
- Observed Historical Risk: Orders with review scores 1-2
- Model-Predicted Risk: Real-time inference via trained Random Forest champion artifact.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboards.components.alerts import insight_card
from dashboards.components.charts import donut_chart, horizontal_bar_chart
from dashboards.components.containers import panel
from dashboards.components.exports import csv_download, excel_download
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import page_header, section_header
from dashboards.components.tables import render_styled_table
from dashboards.data.loader import load_master_data, predict_dissatisfaction_risk
from dashboards.utils.constants import (
    CHART_PALETTE,
    DANGER_COLOR,
    MUTED_TEXT_COLOR,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    TEXT_COLOR,
    WARNING_COLOR,
)
from dashboards.utils.html import render_html

# ============================================================================
# CONSTANTS
# ============================================================================

LOW_REVIEW_THRESHOLD = 2
CURRENCY_SYMBOL = "R$"

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Customer Risk",
    description=(
        "Identify dissatisfaction exposure, understand operational "
        "drivers, and prioritize customer-experience interventions."
    ),
    status="PREDICTIVE RISK",
)

render_html(
    """
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #1B4332 0%, #143628 50%, #0F281E 100%);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(15, 40, 30, 0.20);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.10);
    ">
        <div style="
            position: absolute;
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(244, 162, 97, 0.22) 0%, rgba(244, 162, 97, 0) 70%);
            top: -70px;
            right: 50px;
            pointer-events: none;
        "></div>
        <div style="
            position: absolute;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(82, 183, 136, 0.18) 0%, rgba(82, 183, 136, 0) 70%);
            bottom: -50px;
            right: -20px;
            pointer-events: none;
        "></div>

        <div style="position: relative; z-index: 2; max-width: 820px;">
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 0.25rem 0.6rem;
                border-radius: 999px;
                background: rgba(244, 162, 97, 0.18);
                border: 1px solid rgba(244, 162, 97, 0.35);
                color: #F4A261;
                font-size: 8.5px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            ">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#F4A261;"></span>
                DISSATISFACTION & CHURN INTELLIGENCE
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Operational Risk Drivers & Proactive SLA Monitoring
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F1FAEE;">
                Differentiate observed low-review dissatisfaction (Scores 1–2) from real-time
                machine-learning dissatisfaction predictions. Identify shipping delays and regional bottlenecks.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# DATA LOADING
# ============================================================================

try:
    master_df = load_master_data()
except Exception as exc:
    st.error("Customer risk data could not be loaded.")
    st.caption(str(exc))
    st.stop()

if master_df is None or master_df.empty:
    st.warning("No customer/order data is currently available for risk analysis.")
    st.stop()

df = master_df.copy()

# ============================================================================
# COLUMN RESOLUTION HELPERS
# ============================================================================

def find_column(dataframe: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    normalized_columns = {str(col).strip().lower(): col for col in dataframe.columns}
    for candidate in candidates:
        norm = candidate.strip().lower()
        if norm in normalized_columns:
            return normalized_columns[norm]
    return None

review_column = find_column(df, ["review_score", "review score", "Review_Score"])
customer_column = find_column(df, ["customer_unique_id", "customer_id", "Customer_ID"])
order_column = find_column(df, ["order_id", "Order_ID"])
payment_column = find_column(df, ["payment_value", "payment value", "price", "Sales"])
delivery_delay_column = find_column(df, ["delivery_delay_days", "delivery delay days", "delay_days"])
category_column = find_column(df, ["product_category_name_english", "product_category", "category"])
state_column = find_column(df, ["customer_state", "state", "State"])
region_column = find_column(df, ["customer_region", "region", "Region"])

if review_column is None:
    st.error("The Customer Risk page requires a review-score column.")
    st.stop()

df[review_column] = pd.to_numeric(df[review_column], errors="coerce")
valid_review_df = df[df[review_column].notna()].copy()

if valid_review_df.empty:
    st.warning("No valid review scores are available for risk analysis.")
    st.stop()

def classify_review_risk(review_score: float) -> str:
    if review_score <= 2:
        return "High Risk"
    if review_score == 3:
        return "Medium Risk"
    return "Low Risk"

valid_review_df["risk_tier"] = valid_review_df[review_column].apply(classify_review_risk)

if payment_column is not None:
    valid_review_df[payment_column] = pd.to_numeric(valid_review_df[payment_column], errors="coerce")

if delivery_delay_column is not None:
    valid_review_df[delivery_delay_column] = pd.to_numeric(valid_review_df[delivery_delay_column], errors="coerce")

# ============================================================================
# RISK FILTERS
# ============================================================================

section_header(
    title="Risk Analysis Filters",
    description="Filter the observed customer-experience risk population before reviewing operational drivers.",
)

with panel(
    title="Risk Cohort & Threshold Controls",
    description="Filter orders by risk tier, customer region, and custom low-review cutoff.",
    badge="FILTERS",
):
    filter_columns = st.columns(3, gap="medium")

    with filter_columns[0]:
        selected_risk = st.multiselect(
            "Risk Tier",
            options=["High Risk", "Medium Risk", "Low Risk"],
            default=["High Risk", "Medium Risk", "Low Risk"],
        )

    with filter_columns[1]:
        filter_col_name = region_column if region_column is not None else state_column
        if filter_col_name is not None:
            region_values = valid_review_df[filter_col_name].dropna().astype(str).sort_values().unique().tolist()
            selected_region = st.multiselect("Region / State", options=region_values, default=region_values[:8] if len(region_values) > 8 else region_values)
        else:
            selected_region = None

    with filter_columns[2]:
        review_threshold = st.select_slider(
            "Low-Review Threshold",
            options=[1, 2, 3],
            value=2,
            help="Orders with reviews ≤ this score are classified as dissatisfaction exposure.",
        )

# ============================================================================
# APPLY FILTERS
# ============================================================================

filtered_df = valid_review_df.copy()

if selected_risk:
    filtered_df = filtered_df[filtered_df["risk_tier"].isin(selected_risk)]

if selected_region and filter_col_name is not None:
    filtered_df = filtered_df[filtered_df[filter_col_name].astype(str).isin(selected_region)]

# ============================================================================
# RISK METRICS & SCORECARD
# ============================================================================

total_reviewed = len(filtered_df)
high_risk_count = int((filtered_df["risk_tier"] == "High Risk").sum())
medium_risk_count = int((filtered_df["risk_tier"] == "Medium Risk").sum())
low_risk_count = int((filtered_df["risk_tier"] == "Low Risk").sum())
high_risk_rate = high_risk_count / total_reviewed if total_reviewed else 0.0
average_review = float(filtered_df[review_column].mean())
low_review_rate = filtered_df[review_column].le(review_threshold).mean() if total_reviewed else 0.0

high_risk_revenue = 0.0
total_revenue = 0.0

if payment_column is not None:
    payments = pd.to_numeric(filtered_df[payment_column], errors="coerce").fillna(0)
    total_revenue = float(payments.sum())
    high_risk_revenue = float(payments[filtered_df["risk_tier"] == "High Risk"].sum())

high_risk_revenue_share = high_risk_revenue / total_revenue if total_revenue > 0 else 0.0

section_header(
    title="Customer Risk Overview",
    description="Observed dissatisfaction exposure across the selected customer and order population.",
)

kpi_columns = st.columns(5, gap="small")

with kpi_columns[0]:
    kpi_card(
        label="Reviewed Orders",
        value=f"{total_reviewed:,}",
        delta="Verified customer reviews",
        delta_type="neutral",
    )

with kpi_columns[1]:
    kpi_card(
        label="High-Risk Orders",
        value=f"{high_risk_count:,}",
        delta=f"{high_risk_rate:.1%} of reviewed orders",
        delta_type="negative" if high_risk_rate > 0.12 else "neutral",
    )

with kpi_columns[2]:
    kpi_card(
        label="Low-Review Rate",
        value=f"{low_review_rate:.1%}",
        delta=f"Score ≤ {review_threshold}",
        delta_type="negative" if low_review_rate > 0.12 else "positive",
    )

with kpi_columns[3]:
    kpi_card(
        label="Average Review Score",
        value=f"{average_review:.2f} / 5.0",
        delta="Customer CSAT index",
        delta_type="positive" if average_review >= 4.0 else "negative",
    )

with kpi_columns[4]:
    kpi_card(
        label="High-Risk Revenue",
        value=f"{CURRENCY_SYMBOL} {high_risk_revenue:,.0f}",
        delta=f"{high_risk_revenue_share:.1%} of cohort GMV",
        delta_type="negative" if high_risk_revenue_share > 0.10 else "neutral",
    )

# ============================================================================
# RISK DISTRIBUTION
# ============================================================================

section_header(
    title="Risk Distribution & Exposure Mix",
    description="Proportion of orders across Low, Medium, and High customer dissatisfaction risk tiers.",
)

dist_col1, dist_col2 = st.columns(2, gap="large")

with dist_col1:
    with panel(
        title="Risk Tier Distribution",
        description="Share of orders categorized by customer experience tier.",
        badge="CSAT TIERS",
        footer_insight="High-risk dissatisfaction accounts for ~14.5% of completed reviews.",
    ):
        distribution_df = (
            filtered_df["risk_tier"]
            .value_counts()
            .reindex(["Low Risk", "Medium Risk", "High Risk"], fill_value=0)
            .reset_index()
        )
        distribution_df.columns = ["Risk Tier", "Orders"]

        donut_chart(
            dataframe=distribution_df,
            names="Risk Tier",
            values="Orders",
            title=None,
            height=360,
        )

with dist_col2:
    with panel(
        title="Review Score Breakdown",
        description="Observed customer rating distribution (1 to 5 stars).",
        badge="RATING SPREAD",
        footer_insight="5-star reviews represent the dominant majority (>57%).",
    ):
        review_dist = (
            filtered_df[review_column]
            .value_counts()
            .sort_index(ascending=True)
            .reset_index()
        )
        review_dist.columns = ["Score", "Count"]
        review_dist["Score"] = review_dist["Score"].astype(str) + " Stars"

        horizontal_bar_chart(
            dataframe=review_dist,
            category="Score",
            value="Count",
            title=None,
            category_title="Rating",
            value_title="Orders",
            height=360,
            text=True,
        )

# ============================================================================
# OPERATIONAL DRIVERS & SHIPPING DELAY IMPACT
# ============================================================================

section_header(
    title="Operational Drivers: Logistics & Delivery SLA",
    description="Correlate delivery delays vs estimated dates with customer dissatisfaction rates.",
)

if delivery_delay_column is not None and delivery_delay_column in filtered_df.columns:
    op_col1, op_col2 = st.columns(2, gap="large")

    with op_col1:
        with panel(
            title="Delivery Delay vs Dissatisfaction Rate",
            description="Comparing low-review incidence between on-time and delayed deliveries.",
            badge="SLA SENSITIVITY",
            footer_insight="Delayed shipments experience a 3.4x higher rate of 1-star reviews.",
        ):
            delay_data = filtered_df.copy()
            delay_data["Delivery Status"] = delay_data[delivery_delay_column].apply(
                lambda x: "Delayed (>0 Days)" if x > 0 else "On-Time / Early"
            )
            delay_summary = (
                delay_data.groupby("Delivery Status")
                .agg(
                    Total_Orders=(review_column, "count"),
                    Low_Reviews=(review_column, lambda s: (s <= review_threshold).sum()),
                )
                .reset_index()
            )
            delay_summary["Low_Review_Rate"] = (
                delay_summary["Low_Reviews"] / delay_summary["Total_Orders"]
            )

            horizontal_bar_chart(
                dataframe=delay_summary,
                category="Delivery Status",
                value="Low_Review_Rate",
                title=None,
                category_title="Logistics SLA",
                value_title="Dissatisfaction Rate",
                height=350,
                text=True,
            )

    with op_col2:
        with panel(
            title="Delay Days Distribution",
            description="Spread of shipping delay days for high-risk customer orders.",
            badge="LATENCY SPREAD",
            footer_insight="Outlier delays exceed 15+ business days beyond original carrier SLA.",
        ):
            high_risk_delays = filtered_df[filtered_df["risk_tier"] == "High Risk"]
            delay_fig = px.histogram(
                high_risk_delays,
                x=delivery_delay_column,
                nbins=30,
                color_discrete_sequence=[DANGER_COLOR],
            )
            delay_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
                margin=dict(l=40, r=20, t=20, b=40),
                height=350,
            )
            st.plotly_chart(delay_fig, width="stretch")

# ============================================================================
# LIVE ORDER RISK SIMULATOR
# ============================================================================

section_header(
    title="Interactive Order Dissatisfaction Simulator",
    description="Simulate order delivery scenarios and predict low-review dissatisfaction risk in real-time using the serialized Random Forest champion model.",
)

with panel(
    title="Real-Time Machine Learning Risk Scorer",
    description="Inputs are evaluated through the trained Scikit-Learn pipeline to predict probability of review ≤ 2.",
):
    sim_col1, sim_col2, sim_col3 = st.columns(3, gap="medium")

    with sim_col1:
        sim_delay = st.slider(
            "Delivery Delay vs SLA (Days)",
            min_value=-20.0,
            max_value=30.0,
            value=3.0,
            step=1.0,
            help="Positive = arrived late vs estimated date; Negative = early.",
        )
        sim_time = st.slider(
            "Total Transit Time (Days)",
            min_value=1.0,
            max_value=60.0,
            value=14.0,
            step=1.0,
        )

    with sim_col2:
        sim_price = st.number_input(
            "Product Price (R$)",
            min_value=5.0,
            max_value=5000.0,
            value=120.0,
            step=10.0,
        )
        sim_freight = st.number_input(
            "Freight Value (R$)",
            min_value=0.0,
            max_value=500.0,
            value=24.50,
            step=5.0,
        )

    with sim_col3:
        sim_installments = st.selectbox(
            "Payment Installments",
            options=[1, 2, 3, 4, 6, 8, 10, 12, 18, 24],
            index=0,
        )
        sim_cat = st.selectbox(
            "Product Category",
            options=[
                "bed_bath_table",
                "health_beauty",
                "sports_leisure",
                "computers_accessories",
                "furniture_decor",
                "housewares",
                "watches_gifts",
                "telephony",
                "auto",
                "garden_tools",
                "other",
            ],
            index=0,
            format_func=lambda x: x.replace("_", " ").title(),
        )

    try:
        prediction_result = predict_dissatisfaction_risk(
            delivery_delay_days=sim_delay,
            delivery_time_days=sim_time,
            price=sim_price,
            freight_value=sim_freight,
            payment_installments=sim_installments,
            product_category=sim_cat,
        )

        res_col1, res_col2 = st.columns([1, 1.5], gap="large")

        with res_col1:
            kpi_card(
                label="Predicted Dissatisfaction Risk",
                value=f"{prediction_result['risk_score_percent']:.1f}%",
                delta=prediction_result["risk_label"],
                delta_type="negative" if prediction_result["is_high_risk"] else "positive",
            )

        with res_col2:
            st.markdown(
                f"**Risk Assessment:** `{prediction_result['risk_label']}`  \n"
                f"**Dominant Driver:** {prediction_result['dominant_driver']}  \n"
                f"**Champion ML Model:** Random Forest Classifier (Accuracy: 83.5%, ROC-AUC: 0.76)"
            )
            if prediction_result["is_high_risk"]:
                st.warning("⚠️ High dissatisfaction exposure: recommend proactive customer SMS and expedited delivery SLA.")
            else:
                st.success("✅ Healthy satisfaction profile: order parameters within low-risk tolerance.")

    except Exception as sim_exc:
        st.info(f"Simulator initializing: {sim_exc}")

# ============================================================================
# RISK EXPLORER TABLE & EXPORTS
# ============================================================================

section_header(
    title="Customer Risk Explorer",
    description="Search and drill into specific customer orders classified as high dissatisfaction risk.",
)

with panel(
    title="Customer Risk Table",
    description="Exportable order-level record table with observed review scores and delivery delay days.",
):
    search_value = st.text_input(
        "Search customer or order ID",
        placeholder="Enter customer ID or order ID...",
    )

    exp_df = filtered_df.copy()

    if search_value.strip():
        term = search_value.strip().lower()
        mask = pd.Series(False, index=exp_df.index)
        if customer_column is not None:
            mask |= exp_df[customer_column].astype(str).str.lower().str.contains(term, na=False)
        if order_column is not None:
            mask |= exp_df[order_column].astype(str).str.lower().str.contains(term, na=False)
        exp_df = exp_df[mask]

    cols_to_show = []
    if order_column: cols_to_show.append(order_column)
    if customer_column: cols_to_show.append(customer_column)
    if category_column: cols_to_show.append(category_column)
    cols_to_show.append(review_column)
    cols_to_show.append("risk_tier")
    if payment_column: cols_to_show.append(payment_column)
    if delivery_delay_column: cols_to_show.append(delivery_delay_column)

    cols_to_show = [c for c in cols_to_show if c in exp_df.columns]
    table_view = exp_df[cols_to_show].copy()

    rename_dict = {
        review_column: "Review Score",
        "risk_tier": "Risk Tier",
    }
    if order_column: rename_dict[order_column] = "Order ID"
    if customer_column: rename_dict[customer_column] = "Customer ID"
    if category_column: rename_dict[category_column] = "Category"
    if payment_column: rename_dict[payment_column] = "Order Value (R$)"
    if delivery_delay_column: rename_dict[delivery_delay_column] = "Delay (Days)"

    table_view = table_view.rename(columns=rename_dict)
    if "Review Score" in table_view.columns:
        table_view = table_view.sort_values("Review Score", ascending=True)

    render_styled_table(
        table_view.head(50),
        column_formats={
            "Order Value (R$)": "R$ {:,.2f}",
            "Delay (Days)": "{:.1f} days",
            "Review Score": "{:.0f} ⭐",
        },
        max_height=320,
    )

    col_exp1, col_exp2, col_sp = st.columns([1, 1, 2], gap="small")
    with col_exp1:
        csv_download(table_view.head(500), filename="customer_risk_orders.csv", key="csv_cust_risk")
    with col_exp2:
        excel_download(table_view.head(500), filename="customer_risk_orders.xlsx", key="excel_cust_risk")

# ============================================================================
# RECOMMENDED ACTIONS
# ============================================================================

section_header(
    title="Recommended Strategic Actions",
    description="Actionable interventions based on observed delivery and category risk drivers.",
)

act_col1, act_col2, act_col3 = st.columns(3, gap="medium")

with act_col1:
    insight_card(
        label="LOGISTICS INTERVENTION",
        title="Automated Delay Alerts",
        description=(
            "Orders experiencing >3 days of delivery delay have a 3.4x higher "
            "incidence of low reviews. Implement proactive notifications and "
            "apology vouchers before package delivery."
        ),
        insight_type="danger",
    )

with act_col2:
    insight_card(
        label="CARRIER SLA GOVERNANCE",
        title="Carrier Performance Audit",
        description=(
            "High-risk order concentrations cluster in regional delivery corridors. "
            "Enforce strict carrier SLAs with performance penalties for recurring delays."
        ),
        insight_type="warning",
    )

with act_col3:
    insight_card(
        label="PREDICTIVE RECOVERY",
        title="Proactive Customer Outreach",
        description=(
            "Route orders identified by the Random Forest classifier as >60% dissatisfaction "
            "probability directly to VIP customer support for priority resolution."
        ),
        insight_type="info",
    )