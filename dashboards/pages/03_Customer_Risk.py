"""
Customer Risk Dashboard
=======================

Enterprise Predictive Analytics Engine

Purpose
-------
This page provides an analytical view of customer dissatisfaction risk.

The current project defines risk around low customer review scores rather
than bank churn. Orders receiving a review score of 1 or 2 are treated as
low-review / dissatisfaction observations.

The page combines:

- Customer-risk KPIs
- Low-review exposure
- Risk distribution
- Delivery-delay analysis
- Revenue exposure associated with low reviews
- Category-level risk
- Geographic risk
- Customer/order-level risk explorer
- Classification model context
- Actionable retention recommendations

Architecture
------------
Data loading:
    dashboards.data.loader

Business transformations:
    dashboards.data.transformations

Reusable UI:
    dashboards.components.kpi_cards
    dashboards.components.section_headers
    dashboards.components.containers

Visualization:
    Plotly

Important
---------
This page does not train a model.

It also does not invent churn probabilities or synthetic predictions.

Where a classification output is available in the current project data,
it can be incorporated later through the centralized model/prediction layer.
For now, the page correctly distinguishes observed low-review risk from
model-predicted risk.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import (
    page_header,
    section_header,
)
from dashboards.data.loader import load_master_data


# ============================================================================
# CONSTANTS
# ============================================================================

LOW_REVIEW_THRESHOLD = 2

PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#7C3AED"
SUCCESS_COLOR = "#059669"
WARNING_COLOR = "#D97706"
DANGER_COLOR = "#DC2626"
INFO_COLOR = "#0891B2"

TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#475569"
GRID_COLOR = "#E2E8F0"


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="Customer Risk",
    description=(
        "Identify dissatisfaction exposure, understand its operational "
        "drivers, and prioritize customer-experience interventions."
    ),
)


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Load the centralized master dataset.

    Keeping data loading inside the centralized loader preserves the
    project's architecture and avoids hard-coded file paths inside pages.
    """

    return load_master_data()


try:
    master_df = load_data()

except FileNotFoundError as exc:

    st.error(
        "Customer risk data could not be found."
    )

    st.caption(str(exc))

    st.stop()

except Exception as exc:

    st.error(
        "Customer risk data could not be loaded."
    )

    st.caption(str(exc))

    st.stop()


# ============================================================================
# DATA VALIDATION
# ============================================================================

if master_df is None or master_df.empty:

    st.warning(
        "No customer/order data is currently available for risk analysis."
    )

    st.stop()


# Work on a copy so this page never mutates the centralized dataset.
df = master_df.copy()


# ============================================================================
# COLUMN RESOLUTION
# ============================================================================

def find_column(
    dataframe: pd.DataFrame,
    candidates: list[str],
) -> Optional[str]:
    """
    Find the first available column from a list of possible names.

    The project has gone through several dataset/architecture iterations,
    so this helper makes the page resilient to small naming differences.
    """

    normalized_columns = {
        str(column).strip().lower(): column
        for column in dataframe.columns
    }

    for candidate in candidates:

        normalized_candidate = (
            candidate.strip().lower()
        )

        if normalized_candidate in normalized_columns:
            return normalized_columns[
                normalized_candidate
            ]

    return None


review_column = find_column(
    df,
    [
        "review_score",
        "review score",
        "Review_Score",
        "Review Score",
    ],
)

customer_column = find_column(
    df,
    [
        "customer_unique_id",
        "customer_id",
        "Customer_ID",
        "Customer ID",
    ],
)

order_column = find_column(
    df,
    [
        "order_id",
        "Order_ID",
        "Order ID",
    ],
)

payment_column = find_column(
    df,
    [
        "payment_value",
        "payment value",
        "Sales",
        "sales",
    ],
)

delivery_delay_column = find_column(
    df,
    [
        "delivery_delay_days",
        "delivery delay days",
        "delivery_delay",
        "delay_days",
    ],
)

category_column = find_column(
    df,
    [
        "product_category_name_english",
        "product_category",
        "category",
        "Category",
        "category_name",
    ],
)

state_column = find_column(
    df,
    [
        "customer_state",
        "state",
        "State",
    ],
)

region_column = find_column(
    df,
    [
        "customer_region",
        "region",
        "Region",
    ],
)


# ============================================================================
# REQUIRED FIELD CHECK
# ============================================================================

if review_column is None:

    st.error(
        "The Customer Risk page requires a review-score column."
    )

    st.info(
        "Expected a field such as 'review_score'. "
        "The current dataset schema does not expose one."
    )

    with st.expander(
        "View detected dataset columns"
    ):

        st.write(
            list(df.columns)
        )

    st.stop()


# ============================================================================
# NUMERIC CLEANUP
# ============================================================================

df[review_column] = pd.to_numeric(
    df[review_column],
    errors="coerce",
)

valid_review_df = df[
    df[review_column].notna()
].copy()


if valid_review_df.empty:

    st.warning(
        "No valid review scores are available for risk analysis."
    )

    st.stop()


# ============================================================================
# RISK CLASSIFICATION
# ============================================================================

def classify_review_risk(
    review_score: float,
) -> str:
    """
    Convert observed review scores into analytical risk tiers.

    This is an observed customer-experience classification, not a
    machine-learning prediction.

    1–2 stars:
        High risk

    3 stars:
        Medium risk

    4–5 stars:
        Low risk
    """

    if review_score <= 2:
        return "High Risk"

    if review_score == 3:
        return "Medium Risk"

    return "Low Risk"


valid_review_df["risk_tier"] = (
    valid_review_df[review_column]
    .apply(classify_review_risk)
)


# ============================================================================
# OPTIONAL NUMERIC FIELDS
# ============================================================================

if payment_column is not None:

    valid_review_df[payment_column] = pd.to_numeric(
        valid_review_df[payment_column],
        errors="coerce",
    )


if delivery_delay_column is not None:

    valid_review_df[delivery_delay_column] = pd.to_numeric(
        valid_review_df[delivery_delay_column],
        errors="coerce",
    )


# ============================================================================
# FILTERS
# ============================================================================

section_header(
    title="Risk Analysis Filters",
    description=(
        "Filter the observed customer-experience risk population "
        "before reviewing operational drivers."
    ),
)


filter_columns = st.columns(
    3,
    gap="medium",
)


# ---------------------------------------------------------------------------
# Risk tier filter
# ---------------------------------------------------------------------------

with filter_columns[0]:

    selected_risk = st.multiselect(
        "Risk Tier",
        options=[
            "High Risk",
            "Medium Risk",
            "Low Risk",
        ],
        default=[
            "High Risk",
            "Medium Risk",
            "Low Risk",
        ],
    )


# ---------------------------------------------------------------------------
# Region filter
# ---------------------------------------------------------------------------

with filter_columns[1]:

    selected_region = None

    if region_column is not None:

        region_values = (
            valid_review_df[
                region_column
            ]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

        selected_region = st.multiselect(
            "Region",
            options=region_values,
            default=region_values,
        )

    elif state_column is not None:

        state_values = (
            valid_review_df[
                state_column
            ]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

        selected_region = st.multiselect(
            "State",
            options=state_values,
            default=state_values,
        )

    else:

        st.caption(
            "Regional filtering is unavailable for this dataset."
        )


# ---------------------------------------------------------------------------
# Review threshold
# ---------------------------------------------------------------------------

with filter_columns[2]:

    review_threshold = st.select_slider(
        "Low-review threshold",
        options=[1, 2, 3],
        value=2,
        help=(
            "Reviews at or below this value are treated as "
            "dissatisfaction exposure."
        ),
    )


# ============================================================================
# APPLY FILTERS
# ============================================================================

filtered_df = valid_review_df.copy()


if selected_risk:

    filtered_df = filtered_df[
        filtered_df["risk_tier"].isin(
            selected_risk
        )
    ]


if selected_region:

    filter_column = (
        region_column
        if region_column is not None
        else state_column
    )

    if filter_column is not None:

        filtered_df = filtered_df[
            filtered_df[
                filter_column
            ]
            .astype(str)
            .isin(selected_region)
        ]


# ============================================================================
# RISK METRICS
# ============================================================================

total_reviewed = len(
    filtered_df
)

high_risk_count = int(
    (
        filtered_df["risk_tier"]
        == "High Risk"
    ).sum()
)

medium_risk_count = int(
    (
        filtered_df["risk_tier"]
        == "Medium Risk"
    ).sum()
)

low_risk_count = int(
    (
        filtered_df["risk_tier"]
        == "Low Risk"
    ).sum()
)

high_risk_rate = (
    high_risk_count / total_reviewed
    if total_reviewed
    else 0.0
)

average_review = float(
    filtered_df[
        review_column
    ].mean()
)

low_review_rate = (
    filtered_df[
        review_column
    ]
    .le(review_threshold)
    .mean()
    if total_reviewed
    else 0.0
)


# ============================================================================
# BUSINESS EXPOSURE
# ============================================================================

high_risk_revenue = 0.0
total_revenue = 0.0

if payment_column is not None:

    payment_values = pd.to_numeric(
        filtered_df[payment_column],
        errors="coerce",
    ).fillna(0)

    total_revenue = float(
        payment_values.sum()
    )

    high_risk_revenue = float(
        payment_values[
            filtered_df["risk_tier"]
            == "High Risk"
        ].sum()
    )


high_risk_revenue_share = (
    high_risk_revenue / total_revenue
    if total_revenue > 0
    else 0.0
)


# ============================================================================
# KPI SECTION
# ============================================================================

section_header(
    title="Customer Risk Overview",
    description=(
        "Observed dissatisfaction exposure across the selected "
        "customer and order population."
    ),
)


kpi_columns = st.columns(
    5,
    gap="small",
)


with kpi_columns[0]:

    kpi_card(
        label="Reviewed Orders",
        value=f"{total_reviewed:,}",
        delta="Orders with valid review scores",
        delta_type="neutral",
    )


with kpi_columns[1]:

    kpi_card(
        label="High-Risk Orders",
        value=f"{high_risk_count:,}",
        delta=f"{high_risk_rate:.1%} of reviewed orders",
        delta_type=(
            "negative"
            if high_risk_rate > 0.10
            else "neutral"
        ),
    )


with kpi_columns[2]:

    kpi_card(
        label="Low-Review Rate",
        value=f"{low_review_rate:.1%}",
        delta=(
            f"Score ≤ {review_threshold}"
        ),
        delta_type=(
            "negative"
            if low_review_rate > 0.10
            else "positive"
        ),
    )


with kpi_columns[3]:

    kpi_card(
        label="Average Review",
        value=f"{average_review:.2f}/5",
        delta="Observed customer experience",
        delta_type=(
            "positive"
            if average_review >= 4
            else "negative"
        ),
    )


with kpi_columns[4]:

    if payment_column is not None:

        kpi_card(
            label="High-Risk Revenue",
            value=f"₹{high_risk_revenue:,.0f}",
            delta=(
                f"{high_risk_revenue_share:.1%} of filtered revenue"
            ),
            delta_type=(
                "negative"
                if high_risk_revenue_share > 0.10
                else "neutral"
            ),
        )

    else:

        kpi_card(
            label="Risk Exposure",
            value=f"{high_risk_rate:.1%}",
            delta="High-risk order share",
            delta_type="negative",
        )


# ============================================================================
# RISK DISTRIBUTION
# ============================================================================

section_header(
    title="Risk Distribution",
    description=(
        "Distribution of observed customer-experience risk "
        "across the filtered population."
    ),
)


distribution_df = (
    filtered_df["risk_tier"]
    .value_counts()
    .reindex(
        [
            "Low Risk",
            "Medium Risk",
            "High Risk",
        ],
        fill_value=0,
    )
    .reset_index()
)

distribution_df.columns = [
    "Risk Tier",
    "Orders",
]


chart_columns = st.columns(
    2,
    gap="medium",
)


# ---------------------------------------------------------------------------
# Donut
# ---------------------------------------------------------------------------

with chart_columns[0]:

    figure = px.pie(
        distribution_df,
        names="Risk Tier",
        values="Orders",
        hole=0.64,
        color="Risk Tier",
        color_discrete_map={
            "Low Risk": SUCCESS_COLOR,
            "Medium Risk": WARNING_COLOR,
            "High Risk": DANGER_COLOR,
        },
    )

    figure.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Orders: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
    )

    figure.update_layout(
        height=380,
        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=TEXT_PRIMARY
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5,
        ),
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Bar chart
# ---------------------------------------------------------------------------

with chart_columns[1]:

    bar_figure = px.bar(
        distribution_df,
        x="Risk Tier",
        y="Orders",
        color="Risk Tier",
        color_discrete_map={
            "Low Risk": SUCCESS_COLOR,
            "Medium Risk": WARNING_COLOR,
            "High Risk": DANGER_COLOR,
        },
        text="Orders",
    )

    bar_figure.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
    )

    bar_figure.update_layout(
        height=380,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=TEXT_PRIMARY
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
        ),
        yaxis=dict(
            title="Orders",
            gridcolor=GRID_COLOR,
        ),
        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10,
        ),
    )

    st.plotly_chart(
        bar_figure,
        use_container_width=True,
    )


# ============================================================================
# DELIVERY RISK
# ============================================================================

if delivery_delay_column is not None:

    section_header(
        title="Operational Risk Drivers",
        description=(
            "Compare delivery performance against observed "
            "customer-review outcomes."
        ),
    )

    operational_df = filtered_df.copy()

    operational_df["Delivery Status"] = (
        operational_df[
            delivery_delay_column
        ]
        .apply(
            lambda value:
            "Delayed"
            if pd.notna(value) and value > 0
            else "On Time"
        )
    )

    delivery_summary = (
        operational_df
        .groupby("Delivery Status")
        .agg(
            Orders=(
                review_column,
                "count",
            ),
            Average_Review=(
                review_column,
                "mean",
            ),
            Low_Review_Rate=(
                review_column,
                lambda values:
                values.le(
                    review_threshold
                ).mean(),
            ),
        )
        .reset_index()
    )

    driver_columns = st.columns(
        2,
        gap="medium",
    )

    with driver_columns[0]:

        delivery_figure = px.bar(
            delivery_summary,
            x="Delivery Status",
            y="Low_Review_Rate",
            color="Delivery Status",
            color_discrete_map={
                "On Time": SUCCESS_COLOR,
                "Delayed": DANGER_COLOR,
            },
            text="Low_Review_Rate",
        )

        delivery_figure.update_traces(
            texttemplate="%{text:.1%}",
            textposition="outside",
        )

        delivery_figure.update_layout(
            height=360,
            showlegend=False,
            yaxis=dict(
                title="Low-Review Rate",
                tickformat=".0%",
                gridcolor=GRID_COLOR,
            ),
            xaxis=dict(
                title=None,
                showgrid=False,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10,
            ),
        )

        st.plotly_chart(
            delivery_figure,
            use_container_width=True,
        )

    with driver_columns[1]:

        delivery_display = (
            delivery_summary
            .rename(
                columns={
                    "Delivery Status": "Delivery Status",
                    "Orders": "Orders",
                    "Average_Review": "Avg Review",
                    "Low_Review_Rate": "Low Review Rate",
                }
            )
        )

        delivery_display[
            "Avg Review"
        ] = delivery_display[
            "Avg Review"
        ].round(2)

        delivery_display[
            "Low Review Rate"
        ] = (
            delivery_display[
                "Low Review Rate"
            ]
            .map(
                lambda value:
                f"{value:.1%}"
            )
        )

        st.dataframe(
            delivery_display,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================================
# CATEGORY RISK
# ============================================================================

if category_column is not None:

    section_header(
        title="Category Risk Concentration",
        description=(
            "Identify product categories with the highest observed "
            "dissatisfaction exposure."
        ),
    )

    category_summary = (
        filtered_df
        .groupby(category_column)
        .agg(
            Orders=(
                review_column,
                "count",
            ),
            Average_Review=(
                review_column,
                "mean",
            ),
            Low_Review_Rate=(
                review_column,
                lambda values:
                values.le(
                    review_threshold
                ).mean(),
            ),
        )
        .reset_index()
    )

    category_summary = (
        category_summary[
            category_summary["Orders"] >= 10
        ]
        .sort_values(
            "Low_Review_Rate",
            ascending=False,
        )
        .head(12)
    )

    if not category_summary.empty:

        category_figure = px.bar(
            category_summary.sort_values(
                "Low_Review_Rate"
            ),
            x="Low_Review_Rate",
            y=category_column,
            orientation="h",
            color="Low_Review_Rate",
            color_continuous_scale=[
                "#DBEAFE",
                "#2563EB",
                "#7C3AED",
            ],
            text="Low_Review_Rate",
        )

        category_figure.update_traces(
            texttemplate="%{text:.1%}",
            textposition="outside",
            cliponaxis=False,
        )

        category_figure.update_layout(
            height=460,
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Low-Review Rate",
                tickformat=".0%",
                gridcolor=GRID_COLOR,
            ),
            yaxis=dict(
                title=None,
                showgrid=False,
            ),
            margin=dict(
                l=10,
                r=80,
                t=20,
                b=10,
            ),
        )

        st.plotly_chart(
            category_figure,
            use_container_width=True,
        )


# ============================================================================
# GEOGRAPHIC RISK
# ============================================================================

geo_column = (
    state_column
    if state_column is not None
    else region_column
)


if geo_column is not None:

    section_header(
        title="Geographic Risk",
        description=(
            "Compare dissatisfaction exposure across customer "
            "locations."
        ),
    )

    geographic_summary = (
        filtered_df
        .groupby(geo_column)
        .agg(
            Orders=(
                review_column,
                "count",
            ),
            Average_Review=(
                review_column,
                "mean",
            ),
            Low_Review_Rate=(
                review_column,
                lambda values:
                values.le(
                    review_threshold
                ).mean(),
            ),
        )
        .reset_index()
        .sort_values(
            "Low_Review_Rate",
            ascending=False,
        )
        .head(15)
    )

    geo_figure = px.bar(
        geographic_summary.sort_values(
            "Low_Review_Rate"
        ),
        x="Low_Review_Rate",
        y=geo_column,
        orientation="h",
        color="Low_Review_Rate",
        color_continuous_scale=[
            "#E0F2FE",
            "#0891B2",
            "#7C3AED",
        ],
        text="Low_Review_Rate",
    )

    geo_figure.update_traces(
        texttemplate="%{text:.1%}",
        textposition="outside",
        cliponaxis=False,
    )

    geo_figure.update_layout(
        height=500,
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Low-Review Rate",
            tickformat=".0%",
            gridcolor=GRID_COLOR,
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
        ),
        margin=dict(
            l=10,
            r=80,
            t=20,
            b=10,
        ),
    )

    st.plotly_chart(
        geo_figure,
        use_container_width=True,
    )


# ============================================================================
# CUSTOMER / ORDER RISK EXPLORER
# ============================================================================

section_header(
    title="Risk Explorer",
    description=(
        "Inspect the highest-risk observed orders and customers "
        "for operational follow-up."
    ),
)


explorer_df = filtered_df.copy()


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

search_value = st.text_input(
    "Search customer or order",
    placeholder=(
        "Enter a customer ID or order ID..."
    ),
)


if search_value.strip():

    search_term = (
        search_value
        .strip()
        .lower()
    )

    search_mask = pd.Series(
        False,
        index=explorer_df.index,
    )

    if customer_column is not None:

        search_mask |= (
            explorer_df[
                customer_column
            ]
            .astype(str)
            .str.lower()
            .str.contains(
                search_term,
                na=False,
            )
        )

    if order_column is not None:

        search_mask |= (
            explorer_df[
                order_column
            ]
            .astype(str)
            .str.lower()
            .str.contains(
                search_term,
                na=False,
            )
        )

    explorer_df = explorer_df[
        search_mask
    ]


# ---------------------------------------------------------------------------
# Build display table
# ---------------------------------------------------------------------------

display_columns = []

if order_column is not None:
    display_columns.append(
        order_column
    )

if customer_column is not None:
    display_columns.append(
        customer_column
    )

if category_column is not None:
    display_columns.append(
        category_column
    )

display_columns.extend(
    [
        review_column,
        "risk_tier",
    ]
)

if payment_column is not None:
    display_columns.append(
        payment_column
    )

if delivery_delay_column is not None:
    display_columns.append(
        delivery_delay_column
    )


display_columns = [
    column
    for column in display_columns
    if column in explorer_df.columns
]


risk_table = (
    explorer_df[
        display_columns
    ]
    .copy()
)


rename_map = {
    review_column: "Review Score",
    "risk_tier": "Risk Tier",
}

if payment_column is not None:
    rename_map[
        payment_column
    ] = "Order Value"

if delivery_delay_column is not None:
    rename_map[
        delivery_delay_column
    ] = "Delivery Delay Days"


risk_table = risk_table.rename(
    columns=rename_map
)


# Show highest-risk observations first.

if "Review Score" in risk_table.columns:

    risk_table = risk_table.sort_values(
        "Review Score",
        ascending=True,
    )


st.dataframe(
    risk_table.head(100),
    use_container_width=True,
    hide_index=True,
)


# ============================================================================
# CLASSIFICATION MODEL CONTEXT
# ============================================================================

section_header(
    title="Predictive Model Context",
    description=(
        "Classification models developed in the project for "
        "low-review / dissatisfaction-risk detection."
    ),
)


model_file = (
    "reports/model_comparison_results.csv"
)


try:

    model_results = pd.read_csv(
        model_file
    )

except Exception:

    model_results = pd.DataFrame()


if not model_results.empty:

    # Normalize expected metric names.

    metric_map = {}

    for column in model_results.columns:

        normalized = (
            str(column)
            .strip()
            .lower()
            .replace("_", " ")
        )

        metric_map[
            normalized
        ] = column


    model_column = (
        metric_map.get("model")
    )

    accuracy_column = (
        metric_map.get("accuracy")
    )

    precision_column = (
        metric_map.get("precision")
    )

    recall_column = (
        metric_map.get("recall")
    )

    f1_column = (
        metric_map.get("f1 score")
        or metric_map.get("f1")
    )


    if (
        model_column
        and f1_column
    ):

        results = model_results.copy()

        results[f1_column] = pd.to_numeric(
            results[f1_column],
            errors="coerce",
        )

        results = results.dropna(
            subset=[f1_column]
        )

        if not results.empty:

            results = results.sort_values(
                f1_column,
                ascending=False,
            )

            best_model = str(
                results.iloc[0][
                    model_column
                ]
            )

            best_f1 = float(
                results.iloc[0][
                    f1_column
                ]
            )

            model_columns = st.columns(
                4,
                gap="small",
            )

            with model_columns[0]:

                kpi_card(
                    label="Champion Model",
                    value=best_model,
                    delta="Highest F1 score",
                    delta_type="positive",
                )


            with model_columns[1]:

                kpi_card(
                    label="Best F1",
                    value=f"{best_f1:.2%}",
                    delta="Classification performance",
                    delta_type="positive",
                )


            if (
                accuracy_column
                and accuracy_column
                in results.columns
            ):

                best_accuracy = float(
                    results.iloc[0][
                        accuracy_column
                    ]
                )

                with model_columns[2]:

                    kpi_card(
                        label="Accuracy",
                        value=f"{best_accuracy:.2%}",
                        delta="Champion model",
                        delta_type="neutral",
                    )


            if (
                recall_column
                and recall_column
                in results.columns
            ):

                best_recall = float(
                    results.iloc[0][
                        recall_column
                    ]
                )

                with model_columns[3]:

                    kpi_card(
                        label="Recall",
                        value=f"{best_recall:.2%}",
                        delta="Low-review detection",
                        delta_type="neutral",
                    )


        # ---------------------------------------------------------------
        # Model comparison chart
        # ---------------------------------------------------------------

        metric_columns = []

        if accuracy_column:
            metric_columns.append(
                accuracy_column
            )

        if precision_column:
            metric_columns.append(
                precision_column
            )

        if recall_column:
            metric_columns.append(
                recall_column
            )

        if f1_column:
            metric_columns.append(
                f1_column
            )


        if (
            model_column
            and metric_columns
        ):

            chart_df = results[
                [
                    model_column,
                    *metric_columns,
                ]
            ].copy()

            chart_df = chart_df.rename(
                columns={
                    model_column: "Model"
                }
            )

            melted = chart_df.melt(
                id_vars=["Model"],
                var_name="Metric",
                value_name="Score",
            )

            model_figure = px.bar(
                melted,
                x="Metric",
                y="Score",
                color="Model",
                barmode="group",
                text="Score",
            )

            model_figure.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
            )

            model_figure.update_layout(
                height=420,
                yaxis=dict(
                    title="Score",
                    range=[0, 1.05],
                    gridcolor=GRID_COLOR,
                ),
                xaxis=dict(
                    title=None,
                    showgrid=False,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0,
                ),
                margin=dict(
                    l=10,
                    r=10,
                    t=40,
                    b=10,
                ),
            )

            st.plotly_chart(
                model_figure,
                use_container_width=True,
            )

else:

    st.info(
        "Model comparison results are not currently available. "
        "The risk page is therefore showing observed customer-experience "
        "risk only."
    )


# ============================================================================
# ACTIONABLE INSIGHTS
# ============================================================================

section_header(
    title="Recommended Actions",
    description=(
        "Business actions derived directly from the observed "
        "risk patterns in the selected population."
    ),
)


insight_columns = st.columns(
    3,
    gap="medium",
)


# ---------------------------------------------------------------------------
# Insight 1
# ---------------------------------------------------------------------------

with insight_columns[0]:

    with st.container(
        border=True
    ):

        st.markdown(
            "### ⚠️ Prioritize High-Risk Orders"
        )

        st.write(
            f"{high_risk_count:,} orders are currently "
            f"classified as high-risk based on observed "
            f"review outcomes."
        )

        if high_risk_revenue > 0:

            st.caption(
                f"Associated revenue exposure: "
                f"₹{high_risk_revenue:,.0f}."
            )


# ---------------------------------------------------------------------------
# Insight 2
# ---------------------------------------------------------------------------

with insight_columns[1]:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🚚 Investigate Delivery Experience"
        )

        if (
            delivery_delay_column is not None
            and "delivery_summary"
            in locals()
            and not delivery_summary.empty
        ):

            delayed_row = delivery_summary[
                delivery_summary[
                    "Delivery Status"
                ]
                == "Delayed"
            ]

            if not delayed_row.empty:

                delayed_rate = float(
                    delayed_row.iloc[0][
                        "Low_Review_Rate"
                    ]
                )

                st.write(
                    f"Delayed orders show a "
                    f"{delayed_rate:.1%} low-review rate."
                )

            else:

                st.write(
                    "There are no delayed-order observations "
                    "in the current filtered population."
                )

        else:

            st.write(
                "Delivery-delay data is not available "
                "for deeper operational analysis."
            )


# ---------------------------------------------------------------------------
# Insight 3
# ---------------------------------------------------------------------------

with insight_columns[2]:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🎯 Target Category Hotspots"
        )

        if (
            category_column is not None
            and "category_summary"
            in locals()
            and not category_summary.empty
        ):

            top_category = (
                category_summary.iloc[0]
            )

            st.write(
                f"**{top_category[category_column]}** "
                f"has the highest observed low-review "
                f"rate among categories with sufficient volume."
            )

            st.caption(
                f"Low-review rate: "
                f"{top_category['Low_Review_Rate']:.1%}"
            )

        else:

            st.write(
                "Category-level risk concentration "
                "is not available."
            )


# ============================================================================
# FOOTER NOTE
# ============================================================================

st.caption(
    "Risk definition: observed customer dissatisfaction based on "
    f"review scores ≤ {review_threshold}. "
    "This page does not present synthetic churn probabilities."
)