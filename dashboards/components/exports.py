"""
Reusable data-export components.

Provides centralized CSV and Excel download controls
for dashboard pages.
"""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st


# ============================================================================
# CONSTANTS
# ============================================================================

CSV_MIME_TYPE = "text/csv"

EXCEL_MIME_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# ============================================================================
# VALIDATION
# ============================================================================

def _validate_dataframe(
    dataframe: pd.DataFrame | None,
) -> bool:
    """
    Return True when the supplied DataFrame contains data.
    """

    return (
        dataframe is not None
        and isinstance(dataframe, pd.DataFrame)
        and not dataframe.empty
    )


# ============================================================================
# CSV EXPORT
# ============================================================================

def csv_download(
    dataframe: pd.DataFrame,
    filename: str = "dashboard_data.csv",
    label: str = "Download CSV",
    key: str | None = None,
) -> None:
    """
    Render a CSV download button.
    """

    if not _validate_dataframe(dataframe):

        st.button(
            label,
            disabled=True,
            key=key,
        )

        return

    csv_data = dataframe.to_csv(
        index=False
    )

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime=CSV_MIME_TYPE,
        key=key,
        use_container_width=True,
    )


# ============================================================================
# EXCEL EXPORT
# ============================================================================

def excel_download(
    dataframe: pd.DataFrame,
    filename: str = "dashboard_data.xlsx",
    label: str = "Download Excel",
    sheet_name: str = "Dashboard Data",
    key: str | None = None,
) -> None:
    """
    Render an Excel download button.
    """

    if not _validate_dataframe(dataframe):

        st.button(
            label,
            disabled=True,
            key=key,
        )

        return

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name=sheet_name[:31],
        )

    output.seek(0)

    st.download_button(
        label=label,
        data=output.getvalue(),
        file_name=filename,
        mime=EXCEL_MIME_TYPE,
        key=key,
        use_container_width=True,
    )


# ============================================================================
# EXPORT BUTTON GROUP
# ============================================================================

def export_buttons(
    dataframe: pd.DataFrame,
    filename_prefix: str = "dashboard_data",
    sheet_name: str = "Dashboard Data",
    show_csv: bool = True,
    show_excel: bool = True,
    key_prefix: str = "export",
) -> None:
    """
    Render CSV and Excel export buttons.
    """

    if not show_csv and not show_excel:
        return

    enabled_exports = []

    if show_csv:
        enabled_exports.append("csv")

    if show_excel:
        enabled_exports.append("excel")

    columns = st.columns(
        len(enabled_exports),
        gap="small",
    )

    index = 0

    if show_csv:

        with columns[index]:

            csv_download(
                dataframe=dataframe,
                filename=f"{filename_prefix}.csv",
                label="Download CSV",
                key=f"{key_prefix}_csv",
            )

        index += 1

    if show_excel:

        with columns[index]:

            excel_download(
                dataframe=dataframe,
                filename=f"{filename_prefix}.xlsx",
                label="Download Excel",
                sheet_name=sheet_name,
                key=f"{key_prefix}_excel",
            )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "csv_download",
    "excel_download",
    "export_buttons",
]