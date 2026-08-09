"""
Reusable data-export components.

This module provides centralized download controls for dashboard
data.

Supported formats
-----------------
- CSV
- Excel (.xlsx)

Responsibilities
----------------
- Convert DataFrames into downloadable files.
- Provide consistent download buttons.
- Handle empty datasets safely.
- Keep export logic out of individual dashboard pages.

This module does not:
- calculate business metrics
- filter data
- load source datasets
- modify the original DataFrame
"""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_CSV_MIME = "text/csv"

DEFAULT_EXCEL_MIME = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# ============================================================================
# DATA VALIDATION
# ============================================================================

def _validate_dataframe(
    dataframe: pd.DataFrame | None,
) -> bool:
    """
    Check whether the supplied object is a usable DataFrame.

    Returns
    -------
    bool
        True when a non-empty DataFrame is provided.
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

    Parameters
    ----------
    dataframe:
        DataFrame to export.

    filename:
        Name of the downloaded CSV file.

    label:
        Text displayed on the download button.

    key:
        Optional unique Streamlit widget key.
    """

    if not _validate_dataframe(dataframe):

        st.button(
            label,
            disabled=True,
            key=key,
        )

        return


    # ------------------------------------------------------------------------
    # Convert DataFrame to CSV
    # ------------------------------------------------------------------------

    csv_data = dataframe.to_csv(
        index=False
    )


    # ------------------------------------------------------------------------
    # Render download button
    # ------------------------------------------------------------------------

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime=DEFAULT_CSV_MIME,
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

    Parameters
    ----------
    dataframe:
        DataFrame to export.

    filename:
        Name of the downloaded Excel file.

    label:
        Text displayed on the download button.

    sheet_name:
        Name of the Excel worksheet.

    key:
        Optional unique Streamlit widget key.
    """

    if not _validate_dataframe(dataframe):

        st.button(
            label,
            disabled=True,
            key=key,
        )

        return


    # ------------------------------------------------------------------------
    # Build Excel file in memory
    # ------------------------------------------------------------------------
    #
    # BytesIO avoids creating temporary files on disk.

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


    # Return the buffer to the beginning so Streamlit can read it.
    output.seek(0)


    # ------------------------------------------------------------------------
    # Render download button
    # ------------------------------------------------------------------------

    st.download_button(
        label=label,
        data=output.getvalue(),
        file_name=filename,
        mime=DEFAULT_EXCEL_MIME,
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
    Render a reusable group of export controls.

    Parameters
    ----------
    dataframe:
        DataFrame to export.

    filename_prefix:
        Base filename used for generated files.

    sheet_name:
        Excel worksheet name.

    show_csv:
        Whether to display the CSV export.

    show_excel:
        Whether to display the Excel export.

    key_prefix:
        Prefix used to generate unique Streamlit widget keys.
    """

    if not show_csv and not show_excel:
        return


    columns = []

    if show_csv:
        columns.append("csv")

    if show_excel:
        columns.append("excel")


    export_columns = st.columns(
        len(columns),
        gap="small",
    )


    column_index = 0


    if show_csv:

        with export_columns[column_index]:

            csv_download(
                dataframe=dataframe,
                filename=f"{filename_prefix}.csv",
                label="Download CSV",
                key=f"{key_prefix}_csv",
            )

        column_index += 1


    if show_excel:

        with export_columns[column_index]:

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