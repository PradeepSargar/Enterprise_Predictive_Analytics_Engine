"""
Business transformation layer for the dashboard.

This module converts the order-item master dataset into
reliable business-level metrics.
"""

import pandas as pd


def build_order_level_data(
    master_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert the order-item dataset into one row per order.

    Order-level values such as payment_value can be repeated
    across multiple item rows, so we keep one row per order.
    """

    # Work on a copy so the original dataframe is never modified.
    df = master_df.copy()

    # Sort by order ID for deterministic deduplication.
    df = df.sort_values("order_id")

    # Keep one representative row for every unique order.
    order_df = (
        df.drop_duplicates(
            subset="order_id",
            keep="first",
        )
        .copy()
    )

    return order_df


def calculate_executive_kpis(
    master_df: pd.DataFrame,
) -> dict:
    """
    Calculate the main executive dashboard KPIs.
    """

    # Convert the item-level dataset into order-level data first.
    order_df = build_order_level_data(master_df)

    # Calculate total revenue using one record per order.
    total_revenue = order_df["payment_value"].sum()

    # Count unique orders.
    total_orders = order_df["order_id"].nunique()

    # Count unique customers.
    total_customers = master_df["customer_unique_id"].nunique()

    # Calculate average order value.
    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    # Count orders placed by each customer.
    orders_per_customer = (
        order_df.groupby("customer_unique_id")["order_id"]
        .nunique()
    )

    # Customers with more than one order are repeat customers.
    repeat_customers = (
        orders_per_customer[orders_per_customer > 1]
    )

    # Calculate repeat customer rate.
    repeat_customer_rate = (
        len(repeat_customers) / total_customers
        if total_customers > 0
        else 0
    )

    # Calculate average review score.
    average_review_score = order_df["review_score"].mean()

    # Reviews of 1 or 2 are treated as low reviews.
    low_review_rate = (
        order_df["review_score"].le(2).mean()
    )

    return {
        "total_revenue": float(total_revenue),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "average_order_value": float(average_order_value),
        "repeat_customer_rate": float(repeat_customer_rate),
        "average_review_score": float(average_review_score),
        "low_review_rate": float(low_review_rate),
    }