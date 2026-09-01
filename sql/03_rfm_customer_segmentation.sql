-- ============================================================================
-- 03_rfm_customer_segmentation.sql: Customer-Level RFM Analytics
-- Enterprise Predictive Analytics Engine (Modern Data Stack)
-- ============================================================================
-- Prepares behavioral Recency, Frequency, and Monetary feature matrix per customer
-- relative to the dataset anchor cutoff date (2018-09-01).

CREATE OR REPLACE VIEW v_customer_rfm AS
WITH customer_orders AS (
    SELECT 
        customer_unique_id,
        order_id,
        purchase_timestamp,
        total_order_value
    FROM v_orders_deduplicated
)
SELECT 
    customer_unique_id,
    -- Recency: Days since latest completed order relative to anchor cutoff date (2018-09-01)
    DATEDIFF('day', MAX(purchase_timestamp), TIMESTAMP '2018-09-01 00:00:00') AS recency,
    -- Frequency: Total distinct completed orders
    COUNT(DISTINCT order_id) AS frequency,
    -- Monetary: Total gross spend (rounded)
    ROUND(SUM(total_order_value), 2) AS monetary,
    -- Average Order Value
    ROUND(AVG(total_order_value), 2) AS avg_order_value,
    -- Customer First & Last Purchase Timestamps
    MIN(purchase_timestamp) AS first_purchase_date,
    MAX(purchase_timestamp) AS last_purchase_date
FROM customer_orders
GROUP BY customer_unique_id;
