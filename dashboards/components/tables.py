"""
Reusable professional data-table components.

This module provides presentation-only tables for the
Enterprise Predictive Analytics Engine dashboard.

Tables are rendered using semantic HTML and CSS that guarantees 100% theme
fidelity with the Forest Signal design system across all browsers and devices,
preventing dark-canvas overrides.
"""

from __future__ import annotations

import html
import pandas as pd
import streamlit as st

from dashboards.utils.html import render_html


# ============================================================================
# GENERIC STYLED TABLE RENDERER
# ============================================================================

def render_styled_table(
    dataframe: pd.DataFrame,
    *,
    column_formats: dict[str, str] | None = None,
    column_alignments: dict[str, str] | None = None,
    progress_columns: list[str] | dict[str, float] | None = None,
    max_height: int | None = None,
) -> None:
    """
    Render a DataFrame as a Forest Signal themed table.

    Parameters
    ----------
    dataframe:
        The DataFrame to render.
    column_formats:
        Optional mapping of column names to python format strings, e.g.
        `{"Customers": "{:,.0f}", "Share (%)": "{:.1f}%"}`.
    column_alignments:
        Optional mapping of column names to CSS text-align values ('left', 'right', 'center').
    progress_columns:
        Optional list of column names (or dict mapping name to max value) to render
        with an amber progress bar visual.
    max_height:
        Optional maximum height in pixels with vertical scrolling.
    """
    if dataframe is None or dataframe.empty:
        st.info("No data is available to display.")
        return

    df = dataframe.copy()
    column_formats = column_formats or {}
    column_alignments = column_alignments or {}

    # Normalize progress columns
    progress_dict: dict[str, float] = {}
    if isinstance(progress_columns, list):
        for col in progress_columns:
            if col in df.columns:
                max_val = pd.to_numeric(df[col], errors="coerce").max()
                progress_dict[col] = max_val if pd.notna(max_val) and max_val > 0 else 100.0
    elif isinstance(progress_columns, dict):
        progress_dict = progress_columns

    # Infer alignment: numbers -> right, others -> left
    alignments: dict[str, str] = {}
    for col in df.columns:
        if col in column_alignments:
            alignments[col] = column_alignments[col]
        elif pd.api.types.is_numeric_dtype(df[col]) or col in progress_dict:
            alignments[col] = "right"
        else:
            alignments[col] = "left"

    # Build Header HTML
    header_ths = []
    for col in df.columns:
        align = alignments[col]
        safe_col = html.escape(str(col))
        header_ths.append(
            f'<th style="background-color: #1B4332; color: #F1FAEE; font-weight: 700; '
            f'font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.05em; '
            f'padding: 10px 14px; text-align: {align}; border: none; '
            f'border-bottom: 2px solid #143628; white-space: nowrap;">{safe_col}</th>'
        )
    header_html = "".join(header_ths)

    # Build Rows HTML
    rows_html = []
    for i, (_, row) in enumerate(df.iterrows()):
        row_bg = "#FFFFFF" if i % 2 == 0 else "#F8FCF9"
        tds = []
        for col in df.columns:
            val = row[col]
            align = alignments[col]
            is_first_col = (col == df.columns[0])
            font_weight = "650" if is_first_col else "500"
            text_color = "#112211" if is_first_col else "#2D4A3E"

            # Check for progress bar column
            if col in progress_dict:
                try:
                    num_val = float(val) if pd.notna(val) else 0.0
                    max_v = progress_dict[col]
                    pct = min(max(0.0, (num_val / max_v) * 100.0), 100.0) if max_v > 0 else 0.0
                    if col in column_formats:
                        val_str = column_formats[col].format(val)
                    else:
                        val_str = f"{num_val:.1f}%"
                    safe_val_str = html.escape(val_str)
                    cell_content = (
                        f'<div style="display: inline-flex; align-items: center; justify-content: flex-end; gap: 8px; width: 100%;">'
                        f'<div style="flex: 1; max-width: 80px; height: 6px; background-color: #DEEFE2; border-radius: 999px; overflow: hidden;">'
                        f'<div style="width: {pct:.1f}%; height: 100%; background-color: #F4A261; border-radius: 999px;"></div>'
                        f'</div>'
                        f'<span style="min-width: 44px; text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; color: #112211;">{safe_val_str}</span>'
                        f'</div>'
                    )
                except Exception:
                    cell_content = html.escape(str(val))
            else:
                # Format cell value
                if pd.isna(val):
                    val_str = "—"
                elif col in column_formats:
                    try:
                        val_str = column_formats[col].format(val)
                    except Exception:
                        val_str = str(val)
                elif isinstance(val, (int, float)):
                    if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
                        val_str = f"{int(val):,}"
                    else:
                        val_str = f"{val:,.2f}"
                else:
                    val_str = str(val)
                safe_val_str = html.escape(val_str)
                cell_content = f'<span style="font-variant-numeric: tabular-nums;">{safe_val_str}</span>'

            tds.append(
                f'<td style="padding: 9.5px 14px; border-bottom: 1px solid #C3DFC9; '
                f'color: {text_color}; font-weight: {font_weight}; text-align: {align}; '
                f'font-size: 12.5px; white-space: nowrap;">{cell_content}</td>'
            )

        row_html = (
            f'<tr style="background-color: {row_bg}; transition: background-color 0.15s ease;" '
            f'onmouseover="this.style.backgroundColor=\'#E8F3E8\'" '
            f'onmouseout="this.style.backgroundColor=\'{row_bg}\'">'
            f'{"".join(tds)}'
            f'</tr>'
        )
        rows_html.append(row_html)

    body_html = "".join(rows_html)
    scroll_style = f"max-height: {max_height}px; overflow-y: auto;" if max_height else ""

    table_container_html = f"""
    <div style="width: 100%; overflow-x: auto; {scroll_style} border: 2px solid #C3DFC9; border-radius: 10px; box-shadow: 0 1px 4px rgba(17, 34, 17, 0.05); background-color: #FFFFFF; margin-bottom: 0.5rem;">
        <table style="width: 100%; border-collapse: collapse; background-color: #FFFFFF; font-family: Inter, -apple-system, sans-serif; font-size: 12.5px; margin: 0;">
            <thead>
                <tr>{header_html}</tr>
            </thead>
            <tbody>
                {body_html}
            </tbody>
        </table>
    </div>
    """
    render_html(table_container_html)


# ============================================================================
# CUSTOMER SEGMENT PERFORMANCE TABLE
# ============================================================================

def render_segment_performance_table(
    dataframe: pd.DataFrame,
) -> None:
    """
    Render the customer segment performance table with Forest Signal styling.
    """
    if dataframe is None or dataframe.empty:
        st.info("No segment performance data is available.")
        return

    df = dataframe.copy()
    required_columns = {
        "segment",
        "customers",
        "customer_share",
        "avg_recency",
        "avg_frequency",
        "avg_monetary",
        "total_monetary",
    }

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        st.error(
            "Segment performance table is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )
        return

    numeric_columns = [
        "customers",
        "customer_share",
        "avg_recency",
        "avg_frequency",
        "avg_monetary",
        "total_monetary",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Format customer share as percentage
    display_df = pd.DataFrame(
        {
            "Customer Segment": df["segment"].astype(str),
            "Customers": df["customers"].fillna(0).astype(int),
            "Marketplace Share": df["customer_share"].fillna(0) * 100.0,
            "Avg Recency": df["avg_recency"],
            "Avg Orders": df["avg_frequency"],
            "Avg Spend": df["avg_monetary"],
            "Total GMV": df["total_monetary"],
        }
    )

    render_styled_table(
        display_df,
        column_formats={
            "Customers": "{:,.0f}",
            "Marketplace Share": "{:.1f}%",
            "Avg Recency": "{:,.1f} days",
            "Avg Orders": "{:.2f}",
            "Avg Spend": "R$ {:,.2f}",
            "Total GMV": "R$ {:,.2f}",
        },
        progress_columns=["Marketplace Share"],
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "render_styled_table",
    "render_segment_performance_table",
]