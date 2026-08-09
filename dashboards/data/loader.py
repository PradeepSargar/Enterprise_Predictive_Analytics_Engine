"""
Centralized data-loading layer for the dashboard.

This module is responsible for:

    - Locating project data files safely
    - Loading processed datasets
    - Parsing date columns
    - Caching datasets for better dashboard performance
    - Validating that expected files exist

Pages should import data-loading functions from this module
instead of reading CSV files directly.

This keeps the dashboard architecture clean and maintainable.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# =====================================================================
# PROJECT PATHS
# =====================================================================

# loader.py lives at:
#
# Enterprise Predictive Analytics Engine/
#     dashboards/
#         data/
#             loader.py
#
# parents[0] -> data
# parents[1] -> dashboards
# parents[2] -> project root
#
# Using pathlib makes the application independent of the current
# terminal working directory.

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"


# =====================================================================
# DATA FILES
# =====================================================================

MASTER_DATA_PATH = (
    PROCESSED_DATA_DIR / "olist_master_cleaned.csv"
)

CUSTOMER_SEGMENTS_PATH = (
    PROCESSED_DATA_DIR / "customer_segments.csv"
)

REVENUE_FORECAST_PATH = (
    PROCESSED_DATA_DIR / "revenue_forecast.csv"
)

MODEL_COMPARISON_PATH = (
    REPORTS_DIR / "model_comparison_results.csv"
)


# =====================================================================
# FILE VALIDATION
# =====================================================================

def _validate_file_exists(file_path: Path) -> None:
    """
    Verify that a required project file exists.

    Parameters
    ----------
    file_path:
        Path to the required file.

    Raises
    ------
    FileNotFoundError
        If the required file does not exist.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required dashboard data file was not found:\n"
            f"{file_path}"
        )


# =====================================================================
# MASTER DATA
# =====================================================================

@st.cache_data(show_spinner=False)
def load_master_data() -> pd.DataFrame:
    """
    Load the processed Olist master dataset.

    Returns
    -------
    pandas.DataFrame
        Cleaned master dataset.

    Notes
    -----
    The master dataset is currently at order-item grain.

    This distinction is important because some metrics such as
    revenue and order count must NOT be calculated by blindly
    summing item-level rows.
    """

    _validate_file_exists(MASTER_DATA_PATH)

    df = pd.read_csv(
        MASTER_DATA_PATH,
        low_memory=False,
    )

    # Convert timestamp columns into proper datetime objects.
    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date",
    ]

    for column in datetime_columns:

        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    return df


# =====================================================================
# CUSTOMER SEGMENTS
# =====================================================================

@st.cache_data(show_spinner=False)
def load_customer_segments() -> pd.DataFrame:
    """
    Load the customer RFM segmentation dataset.

    Returns
    -------
    pandas.DataFrame
        Customer-level RFM and clustering results.
    """

    _validate_file_exists(CUSTOMER_SEGMENTS_PATH)

    df = pd.read_csv(
        CUSTOMER_SEGMENTS_PATH,
        low_memory=False,
    )

    return df


# =====================================================================
# REVENUE FORECAST
# =====================================================================

@st.cache_data(show_spinner=False)
def load_revenue_forecast() -> pd.DataFrame:
    """
    Load the revenue forecasting results.

    Returns
    -------
    pandas.DataFrame
        Historical and forecast revenue values including
        lower and upper confidence bounds.
    """

    _validate_file_exists(REVENUE_FORECAST_PATH)

    df = pd.read_csv(
        REVENUE_FORECAST_PATH,
        low_memory=False,
    )

    # The month column is stored as a date-like value in the CSV.
    if "month" in df.columns:

        df["month"] = pd.to_datetime(
            df["month"],
            errors="coerce",
        )

    return df


# =====================================================================
# MODEL COMPARISON
# =====================================================================

@st.cache_data(show_spinner=False)
def load_model_comparison() -> pd.DataFrame:
    """
    Load classification model comparison results.

    Returns
    -------
    pandas.DataFrame
        Accuracy, precision, recall and F1-score for each model.
    """

    _validate_file_exists(MODEL_COMPARISON_PATH)

    df = pd.read_csv(
        MODEL_COMPARISON_PATH,
        low_memory=False,
    )

    return df


# =====================================================================
# DATASET SUMMARY
# =====================================================================

def get_dataset_summary() -> dict:
    """
    Return basic information about the available dashboard datasets.

    This is useful for displaying data-health information later in
    the Data Explorer and Executive Overview pages.
    """

    master_df = load_master_data()
    segments_df = load_customer_segments()
    forecast_df = load_revenue_forecast()

    return {
        "master_rows": len(master_df),
        "master_columns": len(master_df.columns),
        "orders": master_df["order_id"].nunique(),
        "customers": master_df["customer_unique_id"].nunique(),
        "segment_customers": len(segments_df),
        "forecast_periods": len(forecast_df),
    }