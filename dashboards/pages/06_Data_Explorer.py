"""
Data Explorer Dashboard.

This page provides a controlled view of the processed master dataset.

Responsibilities
----------------
1. Load the processed master dataset through the data layer.
2. Display dataset-level statistics.
3. Provide basic data-quality information.
4. Allow users to inspect selected columns.
5. Provide a searchable/filterable data preview.
6. Keep data access and business logic outside the page where possible.

Architecture
------------
Data loading:
    dashboards.data.loader

UI:
    dashboards.components.kpi_cards
    dashboards.components.section_headers
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ============================================================================
# DATA LAYER
# ============================================================================

from dashboards.data.loader import (
    load_master_data,
)


# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

from dashboards.components.kpi_cards import (
    kpi_card,
)

from dashboards.components.section_headers import (
    page_header,
    section_header,
)


# ============================================================================
# PAGE HEADER
# ============================================================================

page_header(
    title="Data Explorer",
    description=(
        "Explore the processed master dataset and review its "
        "structure, quality, and records."
    ),
)


# ============================================================================
# LOAD MASTER DATA
# ============================================================================

try:

    master_df = load_master_data()

except FileNotFoundError as exc:

    st.error(
        "The processed master dataset could not be found."
    )

    st.caption(str(exc))

    st.stop()

except Exception as exc:

    st.error(
        "An unexpected error occurred while loading the master dataset."
    )

    st.caption(str(exc))

    st.stop()


# ============================================================================
# VALIDATE DATA
# ============================================================================

if master_df is None or master_df.empty:

    st.warning(
        "The master dataset is currently empty."
    )

    st.stop()


# ============================================================================
# BASIC DATASET METRICS
# ============================================================================

total_rows = len(master_df)

total_columns = len(master_df.columns)

total_orders = (
    master_df["order_id"].nunique()
    if "order_id" in master_df.columns
    else None
)

total_customers = (
    master_df["customer_unique_id"].nunique()
    if "customer_unique_id" in master_df.columns
    else None
)


# ============================================================================
# DATASET OVERVIEW
# ============================================================================

section_header(
    title="Dataset Overview",
    description=(
        "High-level statistics for the processed master dataset."
    ),
)


kpi_columns = st.columns(
    4,
    gap="large",
)


with kpi_columns[0]:

    kpi_card(
        label="Total Records",
        value=f"{total_rows:,}",
        delta="Dataset rows",
        delta_type="neutral",
    )


with kpi_columns[1]:

    kpi_card(
        label="Columns",
        value=f"{total_columns:,}",
        delta="Available fields",
        delta_type="neutral",
    )


with kpi_columns[2]:

    if total_orders is not None:
        orders_value = f"{total_orders:,}"
    else:
        orders_value = "N/A"

    kpi_card(
        label="Orders",
        value=orders_value,
        delta="Unique orders",
        delta_type="neutral",
    )


with kpi_columns[3]:

    if total_customers is not None:
        customers_value = f"{total_customers:,}"
    else:
        customers_value = "N/A"

    kpi_card(
        label="Customers",
        value=customers_value,
        delta="Unique customers",
        delta_type="neutral",
    )


# ============================================================================
# DATA QUALITY
# ============================================================================

section_header(
    title="Data Quality",
    description=(
        "Review missing values, duplicate records, and dataset completeness."
    ),
)


# ----------------------------------------------------------------------------
# Missing values
# ----------------------------------------------------------------------------

missing_cells = int(
    master_df.isna()
    .sum()
    .sum()
)


total_cells = (
    master_df.shape[0]
    * master_df.shape[1]
)


if total_cells > 0:

    missing_percentage = (
        missing_cells
        / total_cells
    ) * 100

else:

    missing_percentage = 0.0


# ----------------------------------------------------------------------------
# Duplicate rows
# ----------------------------------------------------------------------------

duplicate_rows = int(
    master_df.duplicated()
    .sum()
)


# ----------------------------------------------------------------------------
# Complete rows
# ----------------------------------------------------------------------------

complete_rows = int(
    master_df.notna()
    .all(axis=1)
    .sum()
)


quality_columns = st.columns(
    3,
    gap="large",
)


with quality_columns[0]:

    if missing_percentage == 0:
        missing_delta_type = "positive"
    else:
        missing_delta_type = "negative"

    kpi_card(
        label="Missing Data",
        value=f"{missing_percentage:.2f}%",
        delta=f"{missing_cells:,} missing cells",
        delta_type=missing_delta_type,
    )


with quality_columns[1]:

    if duplicate_rows == 0:
        duplicate_delta_type = "positive"
    else:
        duplicate_delta_type = "negative"

    kpi_card(
        label="Duplicate Rows",
        value=f"{duplicate_rows:,}",
        delta="Exact duplicate records",
        delta_type=duplicate_delta_type,
    )


with quality_columns[2]:

    completeness_percentage = (
        complete_rows
        / total_rows
        * 100
        if total_rows > 0
        else 0
    )

    kpi_card(
        label="Complete Records",
        value=f"{completeness_percentage:.1f}%",
        delta=f"{complete_rows:,} complete rows",
        delta_type="positive",
    )


# ============================================================================
# COLUMN EXPLORER
# ============================================================================

section_header(
    title="Column Explorer",
    description=(
        "Inspect the structure, data type, and missing values "
        "for individual dataset columns."
    ),
)


column_summary = pd.DataFrame(
    {
        "Column": master_df.columns,

        "Data Type": [
            str(dtype)
            for dtype in master_df.dtypes
        ],

        "Non-Null Values": [
            int(master_df[column].notna().sum())
            for column in master_df.columns
        ],

        "Missing Values": [
            int(master_df[column].isna().sum())
            for column in master_df.columns
        ],

        "Missing (%)": [
            master_df[column].isna().mean() * 100
            for column in master_df.columns
        ],

        "Unique Values": [
            int(master_df[column].nunique())
            for column in master_df.columns
        ],
    }
)


st.dataframe(
    column_summary,
    use_container_width=True,
    hide_index=True,
    height=400,
    column_config={

        "Column": st.column_config.TextColumn(
            "Column",
            width="large",
        ),

        "Data Type": st.column_config.TextColumn(
            "Data Type",
            width="medium",
        ),

        "Non-Null Values": st.column_config.NumberColumn(
            "Non-Null Values",
            format="%,d",
        ),

        "Missing Values": st.column_config.NumberColumn(
            "Missing Values",
            format="%,d",
        ),

        "Missing (%)": st.column_config.NumberColumn(
            "Missing (%)",
            format="%.2f%%",
        ),

        "Unique Values": st.column_config.NumberColumn(
            "Unique Values",
            format="%,d",
        ),
    },
)


# ============================================================================
# DATA PREVIEW
# ============================================================================

section_header(
    title="Data Preview",
    description=(
        "Inspect records from the processed master dataset."
    ),
)


# ============================================================================
# PREVIEW CONTROLS
# ============================================================================

control_columns = st.columns(
    [2, 1],
    gap="large",
)


with control_columns[0]:

    selected_columns = st.multiselect(
        "Columns to display",
        options=list(master_df.columns),
        default=list(
            master_df.columns[
                : min(8, len(master_df.columns))
            ]
        ),
    )


with control_columns[1]:

    preview_rows = st.selectbox(
        "Rows to display",
        options=[
            10,
            25,
            50,
            100,
            250,
        ],
        index=2,
    )


# ============================================================================
# SEARCH
# ============================================================================

search_text = st.text_input(
    "Search dataset",
    placeholder="Enter text to search across the selected columns...",
)


# ============================================================================
# BUILD PREVIEW
# ============================================================================

if not selected_columns:

    st.info(
        "Select at least one column to display the data preview."
    )

else:

    preview_df = master_df[
        selected_columns
    ].copy()


    # ------------------------------------------------------------------------
    # Apply text search
    # ------------------------------------------------------------------------

    if search_text.strip():

        search_value = (
            search_text
            .strip()
            .lower()
        )


        # Convert selected columns to strings for a safe,
        # case-insensitive search.

        search_mask = (
            preview_df
            .astype(str)
            .apply(
                lambda column: column.str.lower()
                .str.contains(
                    search_value,
                    na=False,
                )
            )
            .any(axis=1)
        )


        preview_df = preview_df[
            search_mask
        ]


    # ------------------------------------------------------------------------
    # Limit rows
    # ------------------------------------------------------------------------

    preview_df = preview_df.head(
        preview_rows
    )


    # ------------------------------------------------------------------------
    # Display preview
    # ------------------------------------------------------------------------

    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True,
        height=450,
    )


# ============================================================================
# DATASET INFORMATION
# ============================================================================

section_header(
    title="Dataset Information",
    description=(
        "Technical information about the currently loaded dataset."
    ),
)


# ----------------------------------------------------------------------------
# Calculate technical dataset information first.
# ----------------------------------------------------------------------------
#
# Keeping these calculations outside the f-string avoids the formatting
# problem that caused the previous ValueError.

memory_usage_mb = (
    master_df
    .memory_usage(deep=True)
    .sum()
    / (1024 ** 2)
)


datetime_columns = [
    column
    for column in master_df.columns
    if pd.api.types.is_datetime64_any_dtype(
        master_df[column]
    )
]


numeric_columns = len(
    master_df.select_dtypes(
        include="number"
    ).columns
)


categorical_columns = len(
    master_df.select_dtypes(
        include=["object", "category"]
    ).columns
)


# ----------------------------------------------------------------------------
# Display technical information.
# ----------------------------------------------------------------------------

info_columns = st.columns(
    2,
    gap="large",
)


with info_columns[0]:

    st.markdown(
        f"""
**Dataset rows:** {total_rows:,}

**Dataset columns:** {total_columns:,}

**Memory usage:** {memory_usage_mb:.2f} MB
"""
    )


with info_columns[1]:

    st.markdown(
        f"""
**Datetime columns:** {len(datetime_columns):,}

**Numeric columns:** {numeric_columns:,}

**Text / categorical columns:** {categorical_columns:,}
"""
    )