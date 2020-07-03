DROP TABLE IF EXISTS ec_dim_next.product CASCADE;

CREATE TABLE ec_dim_next.product
(
    product_id            TEXT NOT NULL PRIMARY KEY, --unique product identifier

    product_category_fk   INTEGER,                   --root category of product, in Portuguese.

    number_of_photos      INTEGER,                   --number of product published photos
    weight                INTEGER,                   --product weight measured in grams.
    length                INTEGER,                   --product length measured in centimeters.
    height                INTEGER,                   --product height measured in centimeters.
    width                 INTEGER,                   --product width measured in centimeters.

    number_of_orders      INTEGER,
    number_of_order_items INTEGER,
    number_of_customers   INTEGER,
    revenue_all_time      DOUBLE PRECISION,
    total_freight_value   DOUBLE PRECISION,
    avg_days_of_delivery  DOUBLE PRECISION
);

WITH product_items AS (
    SELECT product_id,
           count(*)                               AS number_of_items,
           count(DISTINCT order_item.order_id)    AS number_of_orders,
           count(DISTINCT order_item.customer_id) AS number_of_customers,
           sum(revenue)                           AS revenue_all_time,
           sum(freight_value)                     AS freight_value_all_time,
           avg("order".days_of_delivery)          AS avg_days_of_delivery
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
    GROUP BY product_id
)

INSERT
INTO ec_dim_next.product
SELECT product_id,

       product_category_id                  AS product_category_fk,

       number_of_photos,
       weight,
       length,
       height,
       width,

       product_items.number_of_orders       AS number_of_orders,
       product_items.number_of_items        AS number_of_order_items,
       product_items.number_of_customers    AS number_of_customers,
       product_items.revenue_all_time       AS revenue_all_time,
       product_items.freight_value_all_time AS freight_value_all_time,
       product_items.avg_days_of_delivery   AS avg_days_of_delivery
FROM ec_tmp.product
         LEFT JOIN product_items USING (product_id);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_product()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'product', 'product_category_fk', 'ec_dim_next', 'product_category');
$$
    LANGUAGE sql;

