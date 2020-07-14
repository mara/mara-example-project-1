DROP TABLE IF EXISTS ec_dim_next.customer CASCADE;

CREATE TABLE ec_dim_next.customer
(
    customer_id                TEXT    NOT NULL PRIMARY KEY, -- Unique identifier of a customer
    zip_code_fk                INTEGER NOT NULL,             -- integer representation of a zip_code_prefix
    first_order_fk             TEXT,
    last_order_fk              TEXT,
    favourite_product_category ec_dim_next.PRODUCT_CATEGORY,

    days_since_first_order     INTEGER,
    days_since_last_order      INTEGER,
    lifetime_number_of_orders  INTEGER,
    lifetime_revenue           DOUBLE PRECISION
);

WITH customer_items AS (
    SELECT customer_id,
           count(DISTINCT order_id)                     AS lifetime_number_of_orders,
           sum(product_revenue) + sum(shipping_revenue) AS lifetime_revenue
    FROM ec_tmp.order_item
    GROUP BY customer_id
),
     customer_orders AS (
         SELECT DISTINCT order_item.customer_id,
                         first_value(order_id)
                         OVER (PARTITION BY order_item.customer_id
                             ORDER BY "order".order_date ASC)                     AS first_order_id,
                         first_value(order_id)
                         OVER (PARTITION BY order_item.customer_id
                             ORDER BY "order".order_date DESC)                    AS last_order_id,
                         now() :: DATE
                             - MIN("order".order_date)
                               OVER (PARTITION BY order_item.customer_id) :: DATE AS days_since_first_order,
                         now() :: DATE
                             - MAX("order".order_date)
                               OVER (PARTITION BY order_item.customer_id) :: DATE AS days_since_last_order
         FROM ec_tmp.order_item
                  LEFT JOIN ec_tmp.order USING (order_id)
     ),
     favourite_product_category AS (
         SELECT DISTINCT customer_id, favourite_product_category
         FROM (
                  SELECT order_item.customer_id,
                         product.product_category,
                         sum(order_item.product_revenue),
                         first_value(product.product_category)
                         OVER (PARTITION BY order_item.customer_id
                             ORDER BY sum(product_revenue) DESC) AS favourite_product_category
                  FROM ec_tmp.order_item
                           LEFT JOIN ec_tmp.product USING (product_id)
                  GROUP BY order_item.customer_id, product.product_category
              ) AS t)

INSERT
INTO ec_dim_next.customer
SELECT customer_id,
       zip_code::INTEGER                                                                   AS zip_code_fk,
       customer_orders.first_order_id                                                      AS first_order_fk,
       customer_orders.last_order_id                                                       AS last_order_fk,
       favourite_product_category.favourite_product_category::ec_dim_next.PRODUCT_CATEGORY AS favourite_product_category,
       customer_orders.days_since_first_order                                              AS days_since_first_order,
       customer_orders.days_since_last_order                                               AS days_since_last_order,
       customer_items.lifetime_number_of_orders                                            AS lifetime_number_of_orders,
       customer_items.lifetime_revenue                                                     AS lifetime_revenue

FROM ec_tmp.customer
         LEFT JOIN customer_items USING (customer_id)
         LEFT JOIN customer_orders USING (customer_id)
         LEFT JOIN favourite_product_category USING (customer_id);

SELECT util.add_index('ec_dim_next', 'customer',
                      column_names := ARRAY ['zip_code_fk', 'first_order_fk', 'last_order_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_customer()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'customer', 'ec_dim_next', 'zip_code');
SELECT util.add_fk('ec_dim_next', 'customer', 'first_order_fk', 'ec_dim_next', 'order');
SELECT util.add_fk('ec_dim_next', 'customer', 'last_order_fk', 'ec_dim_next', 'order');
$$
    LANGUAGE sql;
