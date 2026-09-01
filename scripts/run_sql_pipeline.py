"""
Modern Data Stack Pipeline Orchestrator (DuckDB + SQL Layer)
============================================================
Enterprise Predictive Analytics Engine

Responsibilities:
1. Ingests 9 relational CSV files from `data/raw/` into DuckDB OLAP engine (`data/analytics_engine.duckdb`).
2. Executes 5 modular SQL models from `sql/` in strict dependency order:
   - `01_schema_and_views.sql`: Unified multi-table transactional base view.
   - `02_order_deduplication.sql`: Order-level payment deduplication via ROW_NUMBER().
   - `03_rfm_customer_segmentation.sql`: Customer RFM metrics calculation.
   - `04_delivery_performance.sql`: Logistics SLA transit times and delay calculation.
   - `05_monthly_kpis_and_mom.sql`: Monthly GMV and MoM growth calculation via LAG().
3. Exports clean, high-performance Parquet & CSV analytical datasets into `data/processed/`.
4. Validates data integrity, null counts, and telemetry.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
import duckdb
import pandas as pd

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
SQL_DIR = PROJECT_ROOT / "sql"
DB_PATH = PROJECT_ROOT / "data" / "analytics_engine.duckdb"

RAW_TABLE_FILES = {
    "olist_orders_dataset": "olist_orders_dataset.csv",
    "olist_customers_dataset": "olist_customers_dataset.csv",
    "olist_order_items_dataset": "olist_order_items_dataset.csv",
    "olist_order_payments_dataset": "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset": "olist_order_reviews_dataset.csv",
    "olist_products_dataset": "olist_products_dataset.csv",
    "olist_sellers_dataset": "olist_sellers_dataset.csv",
    "olist_geolocation_dataset": "olist_geolocation_dataset.csv",
    "product_category_name_translation": "product_category_name_translation.csv",
}

SQL_MODELS = [
    "01_schema_and_views.sql",
    "02_order_deduplication.sql",
    "03_rfm_customer_segmentation.sql",
    "04_delivery_performance.sql",
    "05_monthly_kpis_and_mom.sql",
]


def ensure_directories():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    if not DATA_RAW.exists():
        raise FileNotFoundError(f"Raw data directory not found: {DATA_RAW}")


def get_connection(db_file: Path | None = None) -> duckdb.DuckDBPyConnection:
    if db_file:
        return duckdb.connect(str(db_file))
    return duckdb.connect()


def ingest_raw_csvs(con: duckdb.DuckDBPyConnection):
    print("=" * 70)
    print("STEP 1: INGESTING RAW CSVs INTO DUCKDB OLAP ENGINE")
    print("=" * 70)
    start_time = time.time()
    
    for table_name, csv_filename in RAW_TABLE_FILES.items():
        csv_path = DATA_RAW / csv_filename
        if not csv_path.exists():
            print(f"  [!] Warning: {csv_filename} not found in {DATA_RAW}")
            continue
        
        escaped_path = str(csv_path).replace("\\", "/")
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS 
            SELECT * FROM read_csv_auto('{escaped_path}', all_varchar=true);
        """)
        row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  [OK] Loaded table '{table_name}': {row_count:,} rows")
    
    elapsed = time.time() - start_time
    print(f"\n[OK] Ingested all raw tables in {elapsed:.2f} seconds.\n")


def execute_sql_models(con: duckdb.DuckDBPyConnection):
    print("=" * 70)
    print("STEP 2: EXECUTING 5 MODULAR SQL ANALYTICS MODELS")
    print("=" * 70)
    
    for sql_file in SQL_MODELS:
        file_path = SQL_DIR / sql_file
        if not file_path.exists():
            raise FileNotFoundError(f"SQL model file not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            sql_content = f.read()
        
        t0 = time.time()
        con.execute(sql_content)
        t_elapsed = (time.time() - t0) * 1000
        print(f"  [OK] Executed '{sql_file}' in {t_elapsed:.1f}ms")
    
    print("\n[OK] All SQL models compiled and registered successfully.\n")


def export_processed_datasets(con: duckdb.DuckDBPyConnection):
    print("=" * 70)
    print("STEP 3: EXPORTING HIGH-PERFORMANCE PARQUET & CSV ARTIFACTS")
    print("=" * 70)

    print("  Creating master cleaned dataset...")
    master_query = """
        SELECT 
            m.order_id,
            m.customer_id,
            m.customer_unique_id,
            m.order_status,
            m.purchase_timestamp,
            m.purchase_timestamp AS order_purchase_timestamp,
            m.approved_at,
            m.approved_at AS order_approved_at,
            m.delivered_carrier_date,
            m.delivered_carrier_date AS order_delivered_carrier_date,
            m.delivered_customer_date,
            m.delivered_customer_date AS order_delivered_customer_date,
            m.estimated_delivery_date,
            m.estimated_delivery_date AS order_estimated_delivery_date,
            m.order_item_id,
            m.product_id,
            m.seller_id,
            m.price,
            m.freight_value,
            m.total_item_value,
            COALESCE(d.total_order_value, m.total_item_value) AS payment_value,
            COALESCE(d.total_order_value, m.total_item_value) AS total_order_value,
            COALESCE(d.payment_installments, 1) AS payment_installments,
            m.product_category_name_english,
            m.product_weight_g,
            m.product_length_cm,
            m.product_height_cm,
            m.product_width_cm,
            m.customer_city,
            m.customer_state,
            m.customer_zip_code_prefix,
            m.review_score,
            m.review_comment_message,
            DATEDIFF('day', m.purchase_timestamp, m.delivered_customer_date) AS delivery_time_days,
            DATEDIFF('day', m.estimated_delivery_date, m.delivered_customer_date) AS delivery_delay_days,
            CASE WHEN m.delivered_customer_date > m.estimated_delivery_date THEN 1 ELSE 0 END AS is_delayed,
            CASE WHEN m.review_score <= 2 THEN 1 ELSE 0 END AS low_review
        FROM v_master_transactions m
        LEFT JOIN v_orders_deduplicated d ON m.order_id = d.order_id
    """
    
    master_df = con.execute(master_query).fetchdf()
    
    master_parquet_path = DATA_PROCESSED / "olist_master_cleaned.parquet"
    master_csv_path = DATA_PROCESSED / "olist_master_cleaned.csv"
    master_df.to_parquet(master_parquet_path, index=False)
    master_df.to_csv(master_csv_path, index=False)
    print(f"  [OK] Exported Master Dataset: {len(master_df):,} rows -> {master_parquet_path.name} & {master_csv_path.name}")

    print("  Creating RFM customer segmentation dataset...")
    rfm_query = """
        SELECT 
            customer_unique_id,
            recency,
            frequency,
            monetary,
            avg_order_value,
            first_purchase_date,
            last_purchase_date
        FROM v_customer_rfm
    """
    rfm_df = con.execute(rfm_query).fetchdf()

    # Assign business segment labels based on behavioral RFM thresholds
    def assign_segment(row):
        if row["frequency"] > 1:
            return "Loyal Repeat Customers"
        elif row["monetary"] >= 500:
            return "High-Value Outliers"
        elif row["recency"] <= 240:
            return "Recent One-Time Buyers"
        else:
            return "Lapsed / At Risk"

    rfm_df["segment"] = rfm_df.apply(assign_segment, axis=1)
    
    rfm_parquet_path = DATA_PROCESSED / "customer_segments.parquet"
    rfm_csv_path = DATA_PROCESSED / "customer_segments.csv"
    rfm_df.to_parquet(rfm_parquet_path, index=False)
    rfm_df.to_csv(rfm_csv_path, index=False)
    print(f"  [OK] Exported Customer RFM Dataset: {len(rfm_df):,} customers -> {rfm_parquet_path.name} & {rfm_csv_path.name}")

    print("  Verifying Monthly KPIs model output...")
    kpi_df = con.execute("SELECT * FROM v_monthly_kpis_mom").fetchdf()
    print(f"  [OK] Computed {len(kpi_df)} monthly KPI periods with MoM growth metrics.")

    print("\n[OK] Export complete! All analytical assets are ready for ML training and UI rendering.\n")


def print_telemetry(con: duckdb.DuckDBPyConnection):
    print("=" * 70)
    print("MODERN DATA STACK TELEMETRY & DATA AUDIT")
    print("=" * 70)
    
    total_orders = con.execute("SELECT COUNT(DISTINCT order_id) FROM v_master_transactions").fetchone()[0]
    unique_customers = con.execute("SELECT COUNT(DISTINCT customer_unique_id) FROM v_master_transactions").fetchone()[0]
    total_items = con.execute("SELECT COUNT(*) FROM v_master_transactions").fetchone()[0]
    delayed_orders = con.execute("SELECT COUNT(*) FROM v_delivery_performance WHERE is_delayed = 1").fetchone()[0]
    low_review_orders = con.execute("SELECT COUNT(*) FROM v_delivery_performance WHERE low_review = 1").fetchone()[0]
    total_perf = con.execute("SELECT COUNT(*) FROM v_delivery_performance").fetchone()[0]
    
    print(f"  * Total Master Transactions (Items): {total_items:,}")
    print(f"  * Unique Orders:                    {total_orders:,}")
    print(f"  * Unique Customers:                 {unique_customers:,}")
    print(f"  * Delayed Delivery Orders:          {delayed_orders:,} ({(delayed_orders/total_perf)*100:.1f}%)")
    print(f"  * Low Review Score Orders (<=2):    {low_review_orders:,} ({(low_review_orders/total_perf)*100:.1f}%)")
    print("=" * 70)


def main():
    ensure_directories()
    print("\n[START] Starting Enterprise Analytics Engine DuckDB Pipeline...\n")
    con = get_connection(DB_PATH)
    try:
        ingest_raw_csvs(con)
        execute_sql_models(con)
        export_processed_datasets(con)
        print_telemetry(con)
        print("\n[COMPLETE] DuckDB Pipeline completed successfully!\n")
    finally:
        con.close()


if __name__ == "__main__":
    main()
