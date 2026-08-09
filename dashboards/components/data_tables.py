"""
Reusable data-table components.

This module contains presentation helpers for dashboard tables.

Design principles
-----------------
- No business logic.
- No data loading.
- No custom HTML tables.
- Tables use Streamlit's native dataframe renderer.
- Formatting is centralized so multiple dashboard pages can reuse it.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# GENERIC DATA TABLE
# ============================================================================

def render_data_table(
    dataframe: pd.DataFrame,
    *,
    height: int = 300,
    hide_index: bool = True,
) -> None:
    """
    Render a reusable dashboard data table.

    Parameters
    ----------
    dataframe:
        DataFrame that should be displayed.

    height:
        Height of the table in pixels.

    hide_index:
        Whether the pandas index should be hidden.
    """

    # ------------------------------------------------------------------------
    # Validate dataframe
    # ------------------------------------------------------------------------

    if dataframe is None or dataframe.empty:

        st.info(
            "No data is available to display."
        )

        return


    # ------------------------------------------------------------------------
    # Render native Streamlit table
    # ------------------------------------------------------------------------

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=hide_index,
        height=height,
    )


# ============================================================================
# CUSTOMER SEGMENT PERFORMANCE TABLE
# ============================================================================

def render_segment_performance_table(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render the customer segment performance table.

    Expected columns
    ----------------
    segment
    customers
    customer_share
    avg_recency
    avg_frequency
    avg_monetary
    total_monetary
    """

    # ------------------------------------------------------------------------
    # Validate dataframe
    # ------------------------------------------------------------------------

    if dataframe is None or dataframe.empty:

        st.info(
            "No segment performance data is available."
        )

        return


    # ------------------------------------------------------------------------
    # Required columns
    # ------------------------------------------------------------------------

    required_columns = {
        "segment",
        "customers",
        "customer_share",
        "avg_recency",
        "avg_frequency",
        "avg_monetary",
        "total_monetary",
    }


    missing_columns = (
        required_columns
        - set(dataframe.columns)
    )


    if missing_columns:

        st.error(
            "Segment performance table is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

        return


    # ------------------------------------------------------------------------
    # Work on a copy
    # ------------------------------------------------------------------------

    display_df = dataframe[
        [
            "segment",
            "customers",
            "customer_share",
            "avg_recency",
            "avg_frequency",
            "avg_monetary",
            "total_monetary",
        ]
    ].copy()


    # ------------------------------------------------------------------------
    # Rename columns for business users
    # ------------------------------------------------------------------------

    display_df = display_df.rename(
        columns={
            "segment": "Customer Segment",
            "customers": "Customers",
            "customer_share": "Customer Share (%)",
            "avg_recency": "Avg Recency (Days)",
            "avg_frequency": "Avg Frequency",
            "avg_monetary": "Avg Monetary Value",
            "total_monetary": "Total Monetary Value",
        }
    )


    # ------------------------------------------------------------------------
    # Convert numeric columns
    # ------------------------------------------------------------------------

    numeric_columns = [
        "Customers",
        "Customer Share (%)",
        "Avg Recency (Days)",
        "Avg Frequency",
        "Avg Monetary Value",
        "Total Monetary Value",
    ]


    for column in numeric_columns:

        display_df[column] = pd.to_numeric(
            display_df[column],
            errors="coerce",
        )


    # ------------------------------------------------------------------------
    # Convert customer share from decimal to percentage
    # ------------------------------------------------------------------------

    display_df["Customer Share (%)"] = (
        display_df["Customer Share (%)"] * 100
    )


    # ------------------------------------------------------------------------
    # Render professionally formatted native Streamlit table
    # ------------------------------------------------------------------------

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=250,
        column_config={

            "Customer Segment": st.column_config.TextColumn(
                "Customer Segment",
                width="large",
            ),

            "Customers": st.column_config.NumberColumn(
                "Customers",
                format="%,d",
                width="medium",
            ),

            "Customer Share (%)": st.column_config.NumberColumn(
                "Customer Share (%)",
                format="%.1f%%",
                width="medium",
            ),

            "Avg Recency (Days)": st.column_config.NumberColumn(
                "Avg Recency (Days)",
                format="%.1f",
                width="medium",
            ),

            "Avg Frequency": st.column_config.NumberColumn(
                "Avg Frequency",
                format="%.2f",
                width="medium",
            ),

            "Avg Monetary Value": st.column_config.NumberColumn(
                "Avg Monetary Value",
                format="₹%.2f",
                width="medium",
            ),

            "Total Monetary Value": st.column_config.NumberColumn(
                "Total Monetary Value",
                format="₹%.2f",
                width="large",
            ),
        },
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "render_data_table",
    "render_segment_performance_table",
]