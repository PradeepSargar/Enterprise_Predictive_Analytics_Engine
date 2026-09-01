-- ============================================================================
-- 04_delivery_performance.sql: Logistics SLA & Dissatisfaction Risk Features
-- Enterprise Predictive Analytics Engine (Modern Data Stack)
-- ============================================================================
-- Computes actual delivery durations and SLA delivery delays
-- for machine learning risk modeling.

CREATE OR REPLACE VIEW v_delivery_performance AS
SELECT 
    order_id,
    customer_unique_id,
    customer_city,
    customer_state,
    product_category_name_english,
    price,
    freight_value,
    total_order_value,
    payment_installments,
    purchase_timestamp,
    delivered_customer_date,
    estimated_delivery_date,
    
    -- Transit Duration: Days between purchase and delivery
    DATEDIFF('day', purchase_timestamp, delivered_customer_date) AS delivery_time_days,
    
    -- SLA Delay: Positive if delivered AFTER estimated date, 0 or negative if on-time
    DATEDIFF('day', estimated_delivery_date, delivered_customer_date) AS delivery_delay_days,
    
    -- Binary SLA Flag: 1 if delayed past promised date, 0 otherwise
    CASE 
        WHEN delivered_customer_date > estimated_delivery_date THEN 1 
        ELSE 0 
    END AS is_delayed,
    
    review_score,
    
    -- Binary Low Review Target (1 if score <= 2 stars, 0 otherwise)
    CASE 
        WHEN review_score <= 2 THEN 1 
        ELSE 0 
    END AS low_review
FROM v_orders_deduplicated
WHERE delivered_customer_date IS NOT NULL 
  AND estimated_delivery_date IS NOT NULL;
