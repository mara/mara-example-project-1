SELECT order_id,
       customer_id,
       order_status,
       order_purchase_timestamp,
       order_approved_at,
       order_delivered_carrier_date,
       order_delivered_customer_date,
       order_estimated_delivery_date
FROM ecommerce.orders
WHERE order_purchase_timestamp >= to_date('@@first-date@@', 'YYYY-MM-DD')
