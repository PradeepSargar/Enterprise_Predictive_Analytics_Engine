-- ============================================================================
-- 01_schema_and_views.sql: Master Transactional Base View
-- Enterprise Predictive Analytics Engine (Modern Data Stack)
-- ============================================================================
-- Unifies raw relational tables (orders, customers, items, products, sellers, reviews)
-- into a clean, typed transactional view (v_master_transactions).

CREATE OR REPLACE VIEW v_master_transactions AS
SELECT
    -- Order Identifiers & Lifecycle Timestamps
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.order_status,
    TRY_CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchase_timestamp,
    TRY_CAST(o.order_approved_at AS TIMESTAMP) AS approved_at,
    TRY_CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS delivered_carrier_date,
    TRY_CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_date,
    TRY_CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_date,
    
    -- Item & Financial Metrics
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    TRY_CAST(oi.price AS DOUBLE) AS price,
    TRY_CAST(oi.freight_value AS DOUBLE) AS freight_value,
    (TRY_CAST(oi.price AS DOUBLE) + TRY_CAST(oi.freight_value AS DOUBLE)) AS total_item_value,
    
    -- Product Dimension & Category Translation
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category_name_english,
    TRY_CAST(p.product_weight_g AS DOUBLE) AS product_weight_g,
    TRY_CAST(p.product_length_cm AS DOUBLE) AS product_length_cm,
    TRY_CAST(p.product_height_cm AS DOUBLE) AS product_height_cm,
    TRY_CAST(p.product_width_cm AS DOUBLE) AS product_width_cm,
    
    -- Customer Geolocation
    c.customer_city,
    c.customer_state,
    c.customer_zip_code_prefix,
    
    -- Review Score (Deduplicated to latest review per order)
    TRY_CAST(r.review_score AS INTEGER) AS review_score,
    r.review_comment_message
FROM olist_orders_dataset o
JOIN olist_customers_dataset c 
    ON o.customer_id = c.customer_id
JOIN olist_order_items_dataset oi 
    ON o.order_id = oi.order_id
LEFT JOIN olist_products_dataset p 
    ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t 
    ON p.product_category_name = t.product_category_name
LEFT JOIN (
    SELECT 
        order_id, 
        review_score, 
        review_comment_message,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_creation_date DESC) as rn
    FROM olist_order_reviews_dataset
) r ON o.order_id = r.order_id AND r.rn = 1
WHERE o.order_status = 'delivered';