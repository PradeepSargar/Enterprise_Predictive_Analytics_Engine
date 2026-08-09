"""
Reusable professional data-table components.

This module provides presentation-only tables for the
Enterprise Predictive Analytics Engine dashboard.

The table uses Streamlit's native dataframe renderer rather than
custom HTML. This keeps rendering reliable across Streamlit versions
and avoids raw HTML appearing as visible text.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# CUSTOMER SEGMENT PERFORMANCE TABLE
# ============================================================================

def render_segment_performance_table(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render the customer segment performance table.

    Parameters
    ----------
    dataframe:
        Segment-level performance dataframe containing:

        - segment
        - customers
        - customer_share
        - avg_recency
        - avg_frequency
        - avg_monetary
        - total_monetary
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
    # Work on a copy
    # ------------------------------------------------------------------------

    df = dataframe.copy()


    # ------------------------------------------------------------------------
    # Validate required columns
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
        - set(df.columns)
    )


    if missing_columns:

        st.error(
            "Segment performance table is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

        return


    # ------------------------------------------------------------------------
    # Convert numeric values safely
    # ------------------------------------------------------------------------

    numeric_columns = [
        "customers",
        "customer_share",
        "avg_recency",
        "avg_frequency",
        "avg_monetary",
        "total_monetary",
    ]


    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


    # =========================================================================
    # CREATE DISPLAY DATAFRAME
    # =========================================================================

    display_df = pd.DataFrame(
        {
            "Customer Segment": (
                df["segment"]
                .astype(str)
            ),

            "Customers": (
                df["customers"]
                .fillna(0)
                .astype(int)
            ),

            "Customer Share": (
                df["customer_share"]
                .fillna(0)
                * 100
            ),

            "Avg Recency": (
                df["avg_recency"]
            ),

            "Avg Frequency": (
                df["avg_frequency"]
            ),

            "Avg Monetary Value": (
                df["avg_monetary"]
            ),

            "Total Monetary Value": (
                df["total_monetary"]
            ),
        }
    )


    # =========================================================================
    # FORMAT TABLE VALUES
    # =========================================================================

    styled_df = (
        display_df.style

        # ---------------------------------------------------------------
        # Customer count
        # ---------------------------------------------------------------

        .format(
            {
                "Customers": "{:,.0f}",
                "Customer Share": "{:.1f}%",
                "Avg Recency": "{:,.1f} days",
                "Avg Frequency": "{:.2f}",
                "Avg Monetary Value": "₹{:,.2f}",
                "Total Monetary Value": "₹{:,.2f}",
            }
        )

        # ---------------------------------------------------------------
        # Header styling
        # ---------------------------------------------------------------

        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        (
                            "background-color",
                            "#171A22",
                        ),
                        (
                            "color",
                            "#CBD5E1",
                        ),
                        (
                            "font-weight",
                            "600",
                        ),
                        (
                            "font-size",
                            "12px",
                        ),
                        (
                            "text-align",
                            "left",
                        ),
                        (
                            "padding",
                            "12px 14px",
                        ),
                        (
                            "border-bottom",
                            "1px solid #334155",
                        ),
                    ],
                },

                {
                    "selector": "td",
                    "props": [
                        (
                            "padding",
                            "12px 14px",
                        ),
                        (
                            "font-size",
                            "13px",
                        ),
                        (
                            "border-bottom",
                            "1px solid #1E293B",
                        ),
                    ],
                },

                {
                    "selector": "tbody tr:hover",
                    "props": [
                        (
                            "background-color",
                            "#172033",
                        ),
                    ],
                },
            ]
        )

        # ---------------------------------------------------------------
        # Alignment
        # ---------------------------------------------------------------

        .set_properties(
            subset=[
                "Customers",
                "Customer Share",
                "Avg Recency",
                "Avg Frequency",
                "Avg Monetary Value",
                "Total Monetary Value",
            ],
            **{
                "text-align": "right",
                "font-variant-numeric": "tabular-nums",
            },
        )

        .set_properties(
            subset=[
                "Customer Segment",
            ],
            **{
                "font-weight": "600",
            },
        )
    )


    # =========================================================================
    # TABLE CONTAINER
    # =========================================================================

    st.markdown(
        """
        <div
            style="
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                overflow: hidden;
                margin-top: 8px;
                margin-bottom: 12px;
                background: #FFFFFF;
            "
        >
        """,
        unsafe_allow_html=True,
    )


    # =========================================================================
    # RENDER TABLE
    # =========================================================================

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=245,
    )


    # =========================================================================
    # CLOSE CONTAINER
    # =========================================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "render_segment_performance_table",
]