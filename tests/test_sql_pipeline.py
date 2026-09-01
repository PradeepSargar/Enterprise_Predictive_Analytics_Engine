"""
Unit & Integration Tests for DuckDB SQL Analytics Pipeline
==========================================================
Enterprise Predictive Analytics Engine (Modern Data Stack)

Validates:
1. Existence and compilation of all 5 SQL model files.
2. DuckDB database connection and view registration.
3. Master transaction schema, row integrity, and timestamp casting.
4. Order deduplication logic (strict 1:1 order-level granularity).
5. Customer RFM feature engineering metrics.
6. Delivery SLA and dissatisfaction target calculation.
7. Monthly GMV aggregation and LAG() MoM growth calculations.
8. Output Parquet dataset integrity.
"""

from pathlib import Path
import pandas as pd
import pytest

duckdb = pytest.importorskip("duckdb", reason="DuckDB is required for SQL pipeline tests")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "data" / "analytics_engine.duckdb"

EXPECTED_SQL_FILES = [
    "01_schema_and_views.sql",
    "02_order_deduplication.sql",
    "03_rfm_customer_segmentation.sql",
    "04_delivery_performance.sql",
    "05_monthly_kpis_and_mom.sql",
]


class TestSQLPipeline:

    def test_sql_files_exist(self):
        """Verify all 5 modular SQL files exist in sql/ directory."""
        assert SQL_DIR.exists(), f"Missing SQL directory: {SQL_DIR}"
        for filename in EXPECTED_SQL_FILES:
            file_path = SQL_DIR / filename
            assert file_path.exists(), f"Missing SQL model: {filename}"
            assert file_path.stat().st_size > 0, f"Empty SQL file: {filename}"

    def test_duckdb_database_and_views(self):
        """Verify analytics_engine.duckdb has registered all core views."""
        assert DB_PATH.exists(), f"DuckDB database file not found: {DB_PATH}"
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            views = con.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'VIEW'").fetchall()
            view_names = [v[0] for v in views]
            expected_views = [
                "v_master_transactions",
                "v_orders_deduplicated",
                "v_customer_rfm",
                "v_delivery_performance",
                "v_monthly_kpis_mom",
            ]
            for exp in expected_views:
                assert exp in view_names, f"Missing view in DuckDB: {exp}"
        finally:
            con.close()

    def test_master_transactions_view(self):
        """Validate v_master_transactions volume and columns."""
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            res = con.execute("SELECT COUNT(*), COUNT(DISTINCT order_id) FROM v_master_transactions").fetchone()
            total_items, unique_orders = res[0], res[1]
            assert total_items >= 100000, f"Expected >= 100k items, got {total_items}"
            assert unique_orders >= 90000, f"Expected >= 90k unique orders, got {unique_orders}"

            # Check columns
            sample = con.execute("SELECT * FROM v_master_transactions LIMIT 5").fetchdf()
            required_cols = [
                "order_id",
                "customer_unique_id",
                "purchase_timestamp",
                "price",
                "freight_value",
                "product_category_name_english",
                "review_score",
            ]
            for col in required_cols:
                assert col in sample.columns, f"Missing column in master view: {col}"
        finally:
            con.close()

    def test_order_deduplication_granularity(self):
        """Ensure v_orders_deduplicated has strict 1:1 order granularity (no duplicate order_ids)."""
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            res = con.execute("""
                SELECT COUNT(*), COUNT(DISTINCT order_id) 
                FROM v_orders_deduplicated
            """).fetchone()
            total_rows, unique_orders = res[0], res[1]
            assert total_rows == unique_orders, f"Deduplication failed: {total_rows} rows vs {unique_orders} distinct orders"
        finally:
            con.close()

    def test_customer_rfm_metrics(self):
        """Validate RFM metric calculation logic."""
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            rfm = con.execute("""
                SELECT 
                    MIN(recency) AS min_rec,
                    MAX(recency) AS max_rec,
                    MIN(frequency) AS min_freq,
                    MAX(frequency) AS max_freq,
                    MIN(monetary) AS min_mon,
                    AVG(monetary) AS avg_mon
                FROM v_customer_rfm
            """).fetchdf()

            assert rfm["min_rec"].iloc[0] >= 0, "Recency cannot be negative"
            assert rfm["min_freq"].iloc[0] >= 1, "Frequency must be at least 1"
            assert rfm["min_mon"].iloc[0] > 0, "Monetary spend must be positive"
            assert rfm["avg_mon"].iloc[0] > 50, "Average spend should be realistic (> 50 BRL)"
        finally:
            con.close()

    def test_delivery_performance_metrics(self):
        """Validate SLA delay and low review classifications."""
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            perf = con.execute("""
                SELECT 
                    AVG(delivery_time_days) AS avg_transit,
                    AVG(low_review) AS low_review_rate,
                    AVG(is_delayed) AS delay_rate
                FROM v_delivery_performance
            """).fetchdf()

            avg_transit = perf["avg_transit"].iloc[0]
            low_review_rate = perf["low_review_rate"].iloc[0]
            delay_rate = perf["delay_rate"].iloc[0]

            assert 5 <= avg_transit <= 25, f"Unusual average transit time: {avg_transit}"
            assert 0.05 <= low_review_rate <= 0.30, f"Unusual low review rate: {low_review_rate}"
            assert 0.02 <= delay_rate <= 0.20, f"Unusual delay rate: {delay_rate}"
        finally:
            con.close()

    def test_monthly_kpis_mom_growth(self):
        """Validate monthly GMV and LAG() MoM calculations."""
        con = duckdb.connect(str(DB_PATH), read_only=True)
        try:
            kpis = con.execute("SELECT * FROM v_monthly_kpis_mom ORDER BY month ASC").fetchdf()
            assert len(kpis) >= 18, f"Expected >= 18 monthly periods, got {len(kpis)}"
            assert "monthly_revenue" in kpis.columns
            assert "mom_growth_pct" in kpis.columns
            # First month prev_month_revenue should be NULL
            assert pd.isna(kpis["prev_month_revenue"].iloc[0])
            # Subsequent months should have numeric values
            assert not pd.isna(kpis["prev_month_revenue"].iloc[1])
        finally:
            con.close()

    def test_processed_parquet_files(self):
        """Verify exported Parquet datasets exist and are non-empty."""
        master_parquet = DATA_PROCESSED / "olist_master_cleaned.parquet"
        segments_parquet = DATA_PROCESSED / "customer_segments.parquet"

        assert master_parquet.exists(), "Master Parquet file missing"
        assert segments_parquet.exists(), "Customer segments Parquet file missing"

        df_m = pd.read_parquet(master_parquet)
        df_s = pd.read_parquet(segments_parquet)

        assert len(df_m) >= 100000
        assert len(df_s) >= 90000
