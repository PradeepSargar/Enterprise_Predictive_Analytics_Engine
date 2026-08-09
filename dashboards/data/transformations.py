"""
Business transformation layer for the dashboard.

This module converts processed datasets into reliable,
business-level analytical datasets and metrics.

Architecture
------------
Raw / processed data
        ↓
Transformation layer
        ↓
Dashboard-ready business data
        ↓
Dashboard pages

Important
---------
The master Olist dataset is at ORDER-ITEM grain.

Therefore order-level metrics such as revenue, orders, and
average order value must be calculated from deduplicated
order-level data.

Customer-level metrics must similarly be calculated from
customer-level datasets.
"""

from __future__ import annotations

import pandas as pd


# ============================================================================
# ORDER-LEVEL DATA
# ============================================================================


def build_order_level_data(
    master_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert the order-item master dataset into one row per order.

    Parameters
    ----------
    master_df:
        Processed master dataset at order-item grain.

    Returns
    -------
    pandas.DataFrame
        One row per unique order.

    Notes
    -----
    The Olist master dataset contains multiple item rows for
    orders containing multiple products.

    Order-level fields such as payment_value and review_score
    may therefore appear repeatedly.

    Deduplicating by order_id prevents those values from being
    incorrectly counted multiple times.
    """

    if master_df is None:
        raise ValueError("master_df cannot be None.")

    if master_df.empty:
        return master_df.copy()

    required_columns = {
        "order_id",
        "customer_unique_id",
    }

    missing_columns = (
        required_columns
        - set(master_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Master dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Work on a copy so the original dataframe is never modified.
    df = master_df.copy()

    # Sort by order ID to make deduplication deterministic.
    df = df.sort_values("order_id")

    # Keep one representative row per order.
    order_df = (
        df.drop_duplicates(
            subset="order_id",
            keep="first",
        )
        .copy()
    )

    return order_df


# ============================================================================
# EXECUTIVE KPIs
# ============================================================================


def calculate_executive_kpis(
    master_df: pd.DataFrame,
) -> dict:
    """
    Calculate the primary executive dashboard KPIs.

    Returns
    -------
    dict
        Business-level KPI values.
    """

    order_df = build_order_level_data(master_df)

    if order_df.empty:
        return {
            "total_revenue": 0.0,
            "total_orders": 0,
            "total_customers": 0,
            "average_order_value": 0.0,
            "repeat_customer_rate": 0.0,
            "average_review_score": 0.0,
            "low_review_rate": 0.0,
        }

    # ------------------------------------------------------------------------
    # Total Revenue
    # ------------------------------------------------------------------------

    total_revenue = (
        pd.to_numeric(
            order_df["payment_value"],
            errors="coerce",
        )
        .fillna(0)
        .sum()
    )

    # ------------------------------------------------------------------------
    # Total Orders
    # ------------------------------------------------------------------------

    total_orders = (
        order_df["order_id"]
        .nunique()
    )

    # ------------------------------------------------------------------------
    # Total Customers
    # ------------------------------------------------------------------------

    total_customers = (
        master_df["customer_unique_id"]
        .nunique()
    )

    # ------------------------------------------------------------------------
    # Average Order Value
    # ------------------------------------------------------------------------

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0.0
    )

    # ------------------------------------------------------------------------
    # Repeat Customer Rate
    # ------------------------------------------------------------------------

    orders_per_customer = (
        order_df
        .groupby("customer_unique_id")["order_id"]
        .nunique()
    )

    repeat_customers = (
        orders_per_customer[
            orders_per_customer > 1
        ]
    )

    repeat_customer_rate = (
        len(repeat_customers)
        / total_customers
        if total_customers > 0
        else 0.0
    )

    # ------------------------------------------------------------------------
    # Average Review Score
    # ------------------------------------------------------------------------

    average_review_score = (
        pd.to_numeric(
            order_df["review_score"],
            errors="coerce",
        )
        .mean()
    )

    if pd.isna(average_review_score):
        average_review_score = 0.0

    # ------------------------------------------------------------------------
    # Low Review Rate
    # ------------------------------------------------------------------------

    review_series = pd.to_numeric(
        order_df["review_score"],
        errors="coerce",
    )

    valid_reviews = review_series.dropna()

    if valid_reviews.empty:
        low_review_rate = 0.0
    else:
        low_review_rate = valid_reviews.le(2).mean()

    return {
        "total_revenue": float(total_revenue),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "average_order_value": float(average_order_value),
        "repeat_customer_rate": float(repeat_customer_rate),
        "average_review_score": float(
            average_review_score
        ),
        "low_review_rate": float(
            low_review_rate
        ),
    }


# ============================================================================
# MONTHLY BUSINESS PERFORMANCE
# ============================================================================


def calculate_monthly_business_performance(
    master_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate monthly revenue, orders, and average order value.

    Returns
    -------
    pandas.DataFrame
        One row per calendar month containing:

        - month
        - revenue
        - orders
        - average_order_value
    """

    order_df = build_order_level_data(master_df)

    if order_df.empty:
        return pd.DataFrame(
            columns=[
                "month",
                "revenue",
                "orders",
                "average_order_value",
            ]
        )

    required_columns = {
        "order_purchase_timestamp",
        "payment_value",
        "order_id",
    }

    missing_columns = (
        required_columns
        - set(order_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Master dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Ensure timestamp is datetime.
    order_df["order_purchase_timestamp"] = pd.to_datetime(
        order_df["order_purchase_timestamp"],
        errors="coerce",
    )

    # Remove records without a valid purchase date.
    order_df = order_df.dropna(
        subset=["order_purchase_timestamp"]
    )

    if order_df.empty:
        return pd.DataFrame(
            columns=[
                "month",
                "revenue",
                "orders",
                "average_order_value",
            ]
        )

    # Convert timestamps to calendar-month periods.
    order_df["month"] = (
        order_df["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    order_df["payment_value"] = pd.to_numeric(
        order_df["payment_value"],
        errors="coerce",
    ).fillna(0)

    monthly = (
        order_df
        .groupby("month", as_index=False)
        .agg(
            revenue=(
                "payment_value",
                "sum",
            ),
            orders=(
                "order_id",
                "nunique",
            ),
        )
        .sort_values("month")
        .reset_index(drop=True)
    )

    monthly["average_order_value"] = (
        monthly["revenue"]
        / monthly["orders"].replace(
            0,
            pd.NA,
        )
    )

    monthly["average_order_value"] = (
        monthly["average_order_value"]
        .fillna(0)
    )

    return monthly


# ============================================================================
# CUSTOMER SEGMENT SUMMARY
# ============================================================================


def calculate_customer_segment_summary(
    customer_segments_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a customer segment distribution summary.

    Parameters
    ----------
    customer_segments_df:
        Customer-level segmentation dataset.

    Returns
    -------
    pandas.DataFrame
        One row per customer segment containing:

        - segment
        - customers
        - percentage
    """

    if customer_segments_df is None:
        raise ValueError(
            "customer_segments_df cannot be None."
        )

    if customer_segments_df.empty:
        return pd.DataFrame(
            columns=[
                "segment",
                "customers",
                "percentage",
            ]
        )

    if "segment" not in customer_segments_df.columns:
        raise ValueError(
            "Customer segmentation dataset must contain "
            "'segment'."
        )

    summary = (
        customer_segments_df
        .dropna(subset=["segment"])
        .groupby("segment")
        .size()
        .reset_index(name="customers")
    )

    summary = (
        summary
        .sort_values(
            "customers",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    total_customers = summary["customers"].sum()

    if total_customers > 0:
        summary["percentage"] = (
            summary["customers"]
            / total_customers
        )
    else:
        summary["percentage"] = 0.0

    return summary


# ============================================================================
# CUSTOMER SEGMENT PERFORMANCE
# ============================================================================


def calculate_segment_performance(
    customer_segments_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate business performance metrics for each customer segment.

    Parameters
    ----------
    customer_segments_df:
        Customer-level RFM segmentation dataset.

    Returns
    -------
    pandas.DataFrame
        One row per segment containing:

        - segment
        - customers
        - customer_share
        - avg_recency
        - avg_frequency
        - avg_monetary
        - total_monetary

    Notes
    -----
    This function performs only business aggregation.

    It does not modify the original customer segmentation dataset.
    """

    if customer_segments_df is None:
        raise ValueError(
            "customer_segments_df cannot be None."
        )

    if customer_segments_df.empty:
        return pd.DataFrame(
            columns=[
                "segment",
                "customers",
                "customer_share",
                "avg_recency",
                "avg_frequency",
                "avg_monetary",
                "total_monetary",
            ]
        )

    required_columns = {
        "segment",
        "recency",
        "frequency",
        "monetary",
    }

    missing_columns = (
        required_columns
        - set(customer_segments_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Customer segmentation dataset is missing "
            "required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Work on a copy to protect the source dataframe.
    df = customer_segments_df.copy()

    # Convert RFM measures to numeric values safely.
    numeric_columns = [
        "recency",
        "frequency",
        "monetary",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Remove records without a segment.
    df = df.dropna(
        subset=["segment"]
    )

    if df.empty:
        return pd.DataFrame(
            columns=[
                "segment",
                "customers",
                "customer_share",
                "avg_recency",
                "avg_frequency",
                "avg_monetary",
                "total_monetary",
            ]
        )

    # ------------------------------------------------------------------------
    # Aggregate segment-level business metrics.
    # ------------------------------------------------------------------------

    performance = (
        df
        .groupby("segment", as_index=False)
        .agg(
            customers=(
                "segment",
                "size",
            ),
            avg_recency=(
                "recency",
                "mean",
            ),
            avg_frequency=(
                "frequency",
                "mean",
            ),
            avg_monetary=(
                "monetary",
                "mean",
            ),
            total_monetary=(
                "monetary",
                "sum",
            ),
        )
    )

    # ------------------------------------------------------------------------
    # Calculate percentage of the total customer base.
    # ------------------------------------------------------------------------

    total_customers = performance["customers"].sum()

    if total_customers > 0:
        performance["customer_share"] = (
            performance["customers"]
            / total_customers
        )
    else:
        performance["customer_share"] = 0.0

    # Keep the most important business segments first.
    performance = (
        performance
        .sort_values(
            "customers",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    # Reorder columns into a dashboard-friendly structure.
    performance = performance[
        [
            "segment",
            "customers",
            "customer_share",
            "avg_recency",
            "avg_frequency",
            "avg_monetary",
            "total_monetary",
        ]
    ]

    return performance


# ============================================================================
# RFM SUMMARY
# ============================================================================


def calculate_rfm_summary(
    customer_segments_df: pd.DataFrame,
) -> dict:
    """
    Calculate overall RFM summary statistics.

    Parameters
    ----------
    customer_segments_df:
        Customer-level RFM segmentation dataset.

    Returns
    -------
    dict
        Median values for:

        - recency
        - frequency
        - monetary

    Notes
    -----
    Median values are used instead of means because customer
    monetary and frequency distributions can be highly skewed.
    """

    if customer_segments_df is None:
        raise ValueError(
            "customer_segments_df cannot be None."
        )

    if customer_segments_df.empty:
        return {
            "recency_median": 0.0,
            "frequency_median": 0.0,
            "monetary_median": 0.0,
        }

    required_columns = {
        "recency",
        "frequency",
        "monetary",
    }

    missing_columns = (
        required_columns
        - set(customer_segments_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Customer segmentation dataset is missing "
            "required RFM columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Convert values safely to numeric.
    recency = pd.to_numeric(
        customer_segments_df["recency"],
        errors="coerce",
    )

    frequency = pd.to_numeric(
        customer_segments_df["frequency"],
        errors="coerce",
    )

    monetary = pd.to_numeric(
        customer_segments_df["monetary"],
        errors="coerce",
    )

    # Calculate medians while ignoring invalid/missing values.
    recency_median = recency.median()
    frequency_median = frequency.median()
    monetary_median = monetary.median()

    # Replace NaN results with zero so the dashboard never
    # receives an invalid numerical value.
    return {
        "recency_median": float(
            0.0
            if pd.isna(recency_median)
            else recency_median
        ),
        "frequency_median": float(
            0.0
            if pd.isna(frequency_median)
            else frequency_median
        ),
        "monetary_median": float(
            0.0
            if pd.isna(monetary_median)
            else monetary_median
        ),
    }


# ============================================================================
# FORECAST DATA PREPARATION
# ============================================================================


def prepare_revenue_forecast(
    forecast_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Prepare the revenue forecast dataset for dashboard rendering.

    Expected columns
    ----------------
    - month
    - predicted_revenue
    - lower_bound
    - upper_bound
    - actual_revenue

    Returns
    -------
    pandas.DataFrame
        Cleaned and chronologically sorted forecast dataset.
    """

    if forecast_df is None:
        raise ValueError(
            "forecast_df cannot be None."
        )

    if forecast_df.empty:
        return forecast_df.copy()

    required_columns = {
        "month",
        "predicted_revenue",
        "lower_bound",
        "upper_bound",
        "actual_revenue",
    }

    missing_columns = (
        required_columns
        - set(forecast_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Forecast dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    df = forecast_df.copy()

    # Convert the forecast time column to datetime.
    df["month"] = pd.to_datetime(
        df["month"],
        errors="coerce",
    )

    # Convert numerical forecast fields safely.
    numeric_columns = [
        "predicted_revenue",
        "lower_bound",
        "upper_bound",
        "actual_revenue",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Remove invalid dates.
    df = (
        df
        .dropna(
            subset=["month"]
        )
        .sort_values("month")
        .reset_index(drop=True)
    )

    return df


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "build_order_level_data",
    "calculate_executive_kpis",
    "calculate_monthly_business_performance",
    "calculate_customer_segment_summary",
    "calculate_segment_performance",
    "calculate_rfm_summary",
    "prepare_revenue_forecast",
]