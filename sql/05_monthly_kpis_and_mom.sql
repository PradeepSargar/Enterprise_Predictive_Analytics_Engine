-- ============================================================================
-- 05_monthly_kpis_and_mom.sql: Financial Metrics & Month-over-Month Growth
-- Enterprise Predictive Analytics Engine (Modern Data Stack)
-- ============================================================================
-- Calculates Monthly Gross Revenue (GMV), Order Volumes, AOV,
-- and Month-over-Month (MoM) revenue growth using the LAG() window function.

CREATE OR REPLACE VIEW v_monthly_kpis_mom AS
WITH monthly_metrics AS (
    SELECT 
        DATE_TRUNC('month', purchase_timestamp) AS month,
        ROUND(SUM(total_order_value), 2) AS monthly_revenue,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_unique_id) AS unique_customers,
        ROUND(AVG(total_order_value), 2) AS average_order_value
    FROM v_orders_deduplicated
    WHERE purchase_timestamp >= TIMESTAMP '2017-01-01 00:00:00'
      AND purchase_timestamp <= TIMESTAMP '2018-08-31 23:59:59'
    GROUP BY DATE_TRUNC('month', purchase_timestamp)
)
SELECT 
    month,
    monthly_revenue,
    total_orders,
    unique_customers,
    average_order_value,
    -- Previous month revenue using LAG window function
    LAG(monthly_revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
    -- Month-over-Month (MoM) revenue growth percentage
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY month)) / 
        NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY month), 0) * 100, 
        2
    ) AS mom_growth_pct
FROM monthly_metrics
ORDER BY month ASC;
