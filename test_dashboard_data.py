"""
Quick validation test for the dashboard data layer.

This file is temporary and can be deleted after validation.
"""

from dashboards.data.loader import (
    load_customer_segments,
    load_master_data,
    load_model_comparison,
    load_revenue_forecast,
    get_dataset_summary,
)


# Load every processed dataset used by the dashboard.
master_df = load_master_data()
segments_df = load_customer_segments()
forecast_df = load_revenue_forecast()
models_df = load_model_comparison()


print("\n========== DASHBOARD DATA VALIDATION ==========")

print(
    f"Master dataset: "
    f"{master_df.shape[0]:,} rows × "
    f"{master_df.shape[1]} columns"
)

print(
    f"Customer segments: "
    f"{segments_df.shape[0]:,} rows × "
    f"{segments_df.shape[1]} columns"
)

print(
    f"Revenue forecast: "
    f"{forecast_df.shape[0]:,} rows × "
    f"{forecast_df.shape[1]} columns"
)

print(
    f"Model comparison: "
    f"{models_df.shape[0]:,} rows × "
    f"{models_df.shape[1]} columns"
)


print("\n========== DATASET SUMMARY ==========")

summary = get_dataset_summary()

for key, value in summary.items():
    print(f"{key}: {value:,}")


print("\n========== VALIDATION PASSED ==========")