"""
Model Performance Dashboard.
============================
Enterprise Predictive Analytics Engine

This page evaluates the classification models developed for customer dissatisfaction
risk detection, comparing Accuracy, Precision, Recall, F1 Score, and Feature Importances.

Responsibilities:
1. Load model evaluation comparison benchmark results.
2. Rank algorithms and highlight production champion (Random Forest Classifier).
3. Provide grouped metric comparisons across candidate models.
4. Visualize Random Forest feature importances & operational drivers.
5. Export detailed benchmark data.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboards.components.alerts import insight_card
from dashboards.components.charts import bar_chart
from dashboards.components.containers import panel
from dashboards.components.exports import csv_download, excel_download
from dashboards.components.kpi_cards import kpi_card
from dashboards.components.section_headers import page_header, section_header
from dashboards.data.loader import load_classification_model, load_model_comparison
from dashboards.utils.constants import (
    CHART_PALETTE,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    TEXT_COLOR,
)
from dashboards.utils.html import render_html

# ============================================================================
# PAGE HEADER & HERO BANNER
# ============================================================================

page_header(
    title="Model Performance",
    description=(
        "Evaluate and benchmark machine learning models across accuracy, precision, "
        "recall, F1 score, and operational feature importance."
    ),
    status="MLOPS & MODEL GOVERNANCE",
)

render_html(
    """
    <div style="
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 40%, #8B5CF6 100%);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px -4px rgba(14, 165, 233, 0.25);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="position: relative; z-index: 2; max-width: 820px;">
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
                CLASSIFICATION BENCHMARK & MLOPS
            </div>
            <div style="font-size: 17px; font-weight: 900; line-height: 1.3; margin-bottom: 0.35rem; color: #FFFFFF;">
                Algorithm Evaluation & Champion Model Selection
            </div>
            <div style="font-size: 11px; opacity: 0.95; line-height: 1.5; color: #F0F9FF;">
                Compare candidate classification architectures (Logistic Regression, LightGBM, Random Forest)
                trained on Brazilian e-commerce logistics and fulfillment records to detect dissatisfaction risk.
            </div>
        </div>
    </div>
    """
)

# ============================================================================
# LOAD MODEL COMPARISON DATA
# ============================================================================

try:
    model_df = load_model_comparison()
except Exception as exc:
    st.error("Model comparison results could not be loaded.")
    st.caption(str(exc))
    st.stop()

if model_df is None or model_df.empty:
    st.warning("Model comparison results are currently unavailable.")
    st.stop()

metric_columns = ["Accuracy", "Precision", "Recall", "F1 Score"]
model_df = model_df.copy()

for col in metric_columns:
    if col in model_df.columns:
        model_df[col] = pd.to_numeric(model_df[col], errors="coerce")

model_df = model_df.dropna(subset=["Model"])
model_df["Performance Score"] = model_df["F1 Score"]
model_df = model_df.sort_values("Performance Score", ascending=False).reset_index(drop=True)

best_model = model_df.iloc[0]
best_model_name = str(best_model["Model"])
best_accuracy = float(best_model["Accuracy"])
best_precision = float(best_model["Precision"])
best_recall = float(best_model["Recall"])
best_f1 = float(best_model["F1 Score"])

# ============================================================================
# CHAMPION MODEL KPI SCORECARD
# ============================================================================

section_header(
    title="Champion Model Scorecard",
    description="Summary of the strongest classification architecture ranked by optimal F1 score balance.",
)

kpi_columns = st.columns(4, gap="large")

with kpi_columns[0]:
    kpi_card(
        label="Production Champion",
        value=best_model_name,
        delta="Highest F1 balance",
        delta_type="positive",
    )

with kpi_columns[1]:
    kpi_card(
        label="Champion F1 Score",
        value=f"{best_f1:.1%}",
        delta="Balanced Precision/Recall",
        delta_type="positive",
    )

with kpi_columns[2]:
    kpi_card(
        label="Accuracy",
        value=f"{best_accuracy:.1%}",
        delta="Overall correct classification",
        delta_type="neutral",
    )

with kpi_columns[3]:
    kpi_card(
        label="Recall (Sensitivity)",
        value=f"{best_recall:.1%}",
        delta="Low-review capture rate",
        delta_type="neutral",
    )

# ============================================================================
# GROUPED METRIC COMPARISON
# ============================================================================

section_header(
    title="Multi-Metric Benchmark Comparison",
    description="Comprehensive evaluation across Accuracy, Precision, Recall, and F1 Score for all candidate algorithms.",
)

col_bench1, col_bench2 = st.columns([1.5, 1], gap="large")

with col_bench1:
    with panel(
        title="Candidate Algorithm Metric Comparison",
        description="Side-by-side grouped evaluation across all 4 key classification metrics.",
        badge="BENCHMARK",
        footer_insight="Random Forest yields the superior balance between precision and sensitivity (F1: 76.5%).",
    ):
        chart_df = model_df[["Model", *metric_columns]].copy()
        melted = chart_df.melt(id_vars=["Model"], var_name="Metric", value_name="Score")

        fig = px.bar(
            melted,
            x="Metric",
            y="Score",
            color="Model",
            barmode="group",
            text="Score",
            color_discrete_sequence=CHART_PALETTE,
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        fig.update_layout(
            height=390,
            yaxis=dict(title="Score", range=[0, 1.1], gridcolor="#F1F5F9"),
            xaxis=dict(title=None, showgrid=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            margin=dict(l=20, r=20, t=35, b=20),
        )
        st.plotly_chart(fig, width="stretch")

with col_bench2:
    with panel(
        title="F1 Score Ranking",
        description="F1 score comparison indicating model balance.",
        badge="CHAMPION RANKING",
        footer_insight="Random Forest outperforms baseline Logistic Regression and LightGBM models.",
    ):
        f1_df = model_df[["Model", "F1 Score"]].sort_values("F1 Score", ascending=True)
        bar_chart(
            dataframe=f1_df,
            x="Model",
            y="F1 Score",
            title="F1 Score Ranking",
            x_title="Model",
            y_title="F1 Score",
            height=390,
        )

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================

try:
    artifact = load_classification_model()
    if "feature_importances" in artifact and artifact["feature_importances"]:
        fi_df = pd.DataFrame(artifact["feature_importances"]).head(8)
        fi_df["Feature"] = fi_df["feature"].apply(
            lambda x: x.replace("_", " ").replace("cat ", "Category: ").title()
        )
        fi_df["Importance (%)"] = fi_df["importance"] * 100

        section_header(
            title="Random Forest Feature Importance",
            description="Relative influence of operational, delivery, and economic features in driving dissatisfaction predictions.",
        )

        with panel(
            title="Top 8 Predictive Feature Importances",
            description="Permutation and impurity-based importance ranking from the serialized champion pipeline.",
            badge="FEATURE ATTRIBUTION",
            footer_insight="Delivery delay vs estimated date is the primary driver of customer dissatisfaction.",
        ):
            bar_chart(
                dataframe=fi_df,
                x="Feature",
                y="Importance (%)",
                title="Top Predictive Features in Dissatisfaction Classification",
                x_title="Feature",
                y_title="Relative Importance (%)",
                height=380,
            )
except Exception:
    pass

# ============================================================================
# MODEL COMPARISON DETAIL TABLE & EXPORTS
# ============================================================================

section_header(
    title="Model Benchmark Detail Table",
    description="Detailed numerical metrics for every evaluated classification architecture.",
)

with panel(
    title="Classification Benchmarks",
    description="Exportable evaluation table showing Accuracy, Precision, Recall, and F1 Score.",
):
    table_display = model_df[["Model", "Accuracy", "Precision", "Recall", "F1 Score"]].copy()

    st.dataframe(
        table_display,
        width="stretch",
        hide_index=True,
        column_config={
            "Model": st.column_config.TextColumn("Algorithm / Architecture", width="large"),
            "Accuracy": st.column_config.NumberColumn("Accuracy", format="%.2f%%"),
            "Precision": st.column_config.NumberColumn("Precision", format="%.2f%%"),
            "Recall": st.column_config.NumberColumn("Recall (Sensitivity)", format="%.2f%%"),
            "F1 Score": st.column_config.NumberColumn("F1 Score", format="%.2f%%"),
        },
    )

    col_exp1, col_exp2, col_sp = st.columns([1, 1, 2], gap="small")
    with col_exp1:
        csv_download(table_display, filename="model_comparison_benchmark.csv", key="csv_model_cmp")
    with col_exp2:
        excel_download(table_display, filename="model_comparison_benchmark.xlsx", key="excel_model_cmp")