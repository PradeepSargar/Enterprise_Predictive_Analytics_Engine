-- ============================================================================
-- 02_order_deduplication.sql: Order-Level Granularity & Payment Deduplication
-- Enterprise Predictive Analytics Engine (Modern Data Stack)
-- ============================================================================
-- Eliminates duplicate payments and review scores caused by multi-item orders
-- using ROW_NUMBER() window function.

CREATE OR REPLACE VIEW v_orders_deduplicated AS
WITH order_payments_summary AS (
    SELECT 
        order_id,
        TRY_CAST(SUM(TRY_CAST(payment_value AS DOUBLE)) AS DOUBLE) AS total_payment_value,
        TRY_CAST(MAX(TRY_CAST(payment_installments AS INTEGER)) AS INTEGER) AS payment_installments,
        COUNT(DISTINCT payment_type) AS payment_types_count
    FROM olist_order_payments_dataset
    GROUP BY order_id
),
ranked_order_items AS (
    SELECT 
        order_id,
        customer_id,
        customer_unique_id,
        customer_city,
        customer_state,
        customer_zip_code_prefix,
        purchase_timestamp,
        delivered_carrier_date,
        delivered_customer_date,
        estimated_delivery_date,
        review_score,
        product_category_name_english,
        price,
        freight_value,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_item_id ASC) AS rn
    FROM v_master_transactions
)
SELECT 
    r.order_id,
    r.customer_unique_id,
    r.customer_city,
    r.customer_state,
    r.customer_zip_code_prefix,
    r.purchase_timestamp,
    r.delivered_carrier_date,
    r.delivered_customer_date,
    r.estimated_delivery_date,
    r.review_score,
    r.product_category_name_english,
    r.price,
    r.freight_value,
    COALESCE(p.total_payment_value, (r.price + r.freight_value)) AS total_order_value,
    COALESCE(p.payment_installments, 1) AS payment_installments,
    COALESCE(p.payment_types_count, 1) AS payment_types_count
FROM ranked_order_items r
LEFT JOIN order_payments_summary p 
    ON r.order_id = p.order_id
WHERE r.rn = 1;
