DROP TABLE IF EXISTS ec_dim_next.seller CASCADE;

CREATE TABLE ec_dim_next.seller
(
    seller_id                    TEXT    NOT NULL PRIMARY KEY, -- seller unique identifier
    zip_code_fk                  INTEGER NOT NULL,             -- integer representation of a zip_code_prefix
    first_order_fk               TEXT,

    number_of_orders             INTEGER,
    number_of_order_items        INTEGER,
    number_of_deliveries         INTEGER,
    product_revenue              DOUBLE PRECISION,
    shipping_revenue             DOUBLE PRECISION,
    avg_days_of_payment_approval DOUBLE PRECISION
);

WITH seller_items AS (
    SELECT seller_id,
           count(*)                                   AS number_of_items,
           count(DISTINCT order_item.order_id)        AS number_of_orders,
           count(DISTINCT order_item.order_id)
           FILTER ( WHERE delivery_date IS NOT NULL ) AS number_of_deliveries,
           count(DISTINCT order_item.customer_id)     AS number_of_customers,
           sum(product_revenue)                       AS product_revenue,
           sum(shipping_revenue)                      AS shipping_revenue,
           avg(payment_approval_time_in_days)         AS avg_days_of_payment_approval
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
    GROUP BY seller_id
)
   , seller_orders AS (
    SELECT DISTINCT seller_id,
                    first_value(order_id)
                    OVER (PARTITION BY seller_id
                        ORDER BY "order".order_date ASC)  AS first_order_id
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
)

INSERT
INTO ec_dim_next.seller
SELECT seller_id,
       zip_code::INTEGER                         AS zip_code_fk,

       seller_orders.first_order_id              AS first_order_fk,


       seller_items.number_of_orders             AS number_of_orders,
       seller_items.number_of_items              AS number_of_order_items,
       seller_items.number_of_deliveries         AS number_of_deliveries,
       seller_items.product_revenue              AS product_revenue,
       seller_items.shipping_revenue             AS shipping_revenue,
       seller_items.avg_days_of_payment_approval AS avg_days_of_payment_approval
FROM ec_tmp.seller
         LEFT JOIN seller_items USING (seller_id)
         LEFT JOIN seller_orders USING (seller_id);

SELECT util.add_index('ec_dim_next', 'seller', column_names := ARRAY ['seller_id', 'zip_code_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_sellers()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'seller', 'ec_dim_next', 'zip_code');
SELECT util.add_fk('ec_dim_next', 'seller', 'first_order_fk', 'ec_dim_next', 'order');
SELECT util.add_fk('ec_dim_next', 'seller', 'last_order_fk', 'ec_dim_next', 'order');
$$
    LANGUAGE sql;
