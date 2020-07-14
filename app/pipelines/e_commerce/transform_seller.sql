DROP TABLE IF EXISTS ec_dim_next.seller CASCADE;

CREATE TABLE ec_dim_next.seller
(
    seller_id                      TEXT    NOT NULL PRIMARY KEY, -- seller unique identifier
    zip_code_fk                    INTEGER NOT NULL,             -- integer representation of a zip_code_prefix
    first_order_fk                 TEXT,

    lifetime_number_of_orders      INTEGER,
    lifetime_number_of_order_items INTEGER,
    lifetime_sales                 DOUBLE PRECISION
);

WITH seller_items AS (
    SELECT seller_id,
           count(*)                                     AS lifetime_number_of_order_items,
           count(DISTINCT order_item.order_id)          AS lifetime_number_of_orders,
           sum(product_revenue) + sum(shipping_revenue) AS lifetime_sales
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
    GROUP BY seller_id
)
   , seller_orders AS (
    SELECT DISTINCT seller_id,
                    first_value(order_id)
                    OVER (PARTITION BY seller_id
                        ORDER BY "order".order_date ASC) AS first_order_id
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
)

INSERT
INTO ec_dim_next.seller
SELECT seller_id,
       zip_code::INTEGER                           AS zip_code_fk,

       seller_orders.first_order_id                AS first_order_fk,


       seller_items.lifetime_number_of_orders      AS lifetime_number_of_orders,
       seller_items.lifetime_number_of_order_items AS lifetime_number_of_order_items,
       seller_items.lifetime_sales                 AS lifetime_sales
FROM ec_tmp.seller
         LEFT JOIN seller_items USING (seller_id)
         LEFT JOIN seller_orders USING (seller_id);

SELECT util.add_index('ec_dim_next', 'seller', column_names := ARRAY ['seller_id', 'zip_code_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_sellers()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'seller', 'ec_dim_next', 'zip_code');
SELECT util.add_fk('ec_dim_next', 'seller', 'first_order_fk', 'ec_dim_next', 'order');
$$
    LANGUAGE sql;
