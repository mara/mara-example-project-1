DROP TABLE IF EXISTS ec_dim_next.customer CASCADE;

CREATE TABLE ec_dim_next.customer
(
    customer_id           TEXT    NOT NULL PRIMARY KEY, -- Unique identifier of a customer
    zip_code_fk           INTEGER NOT NULL,             -- integer representation of a zip_code_prefix
    first_order_fk        TEXT,
    last_order_fk         TEXT,

    days_since_last_order INTEGER,
    number_of_orders      INTEGER,
    number_of_order_items INTEGER,
    revenue_lifetime      DOUBLE PRECISION,
    total_freight_value   DOUBLE PRECISION
);

WITH customer_items AS (
    SELECT customer_id,
           count(*)                 AS number_of_items,
           count(DISTINCT order_id) AS number_of_orders,
           sum(revenue)             AS revenue_lifetime,
           sum(freight_value)       AS total_freight_value
    FROM ec_tmp.order_item
    GROUP BY customer_id
)
   , customer_orders AS (
    SELECT DISTINCT order_item.customer_id,
                    first_value(order_id)
                    OVER (PARTITION BY order_item.customer_id
                        ORDER BY "order".purchase_date ASC)                  AS first_order_id,
                    first_value(order_id)
                    OVER (PARTITION BY order_item.customer_id
                        ORDER BY "order".purchase_date DESC)                 AS last_order_id,
                    now() :: DATE
                        - MAX("order".purchase_date)
                          OVER (PARTITION BY order_item.customer_id) :: DATE AS days_since_last_order
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
)

INSERT
INTO ec_dim_next.customer
SELECT customer_id,
       zip_code.zip_code_id                  AS zip_code_fk,
       customer_orders.first_order_id        AS first_order_fk,
       customer_orders.last_order_id         AS last_order_fk,

       customer_orders.days_since_last_order AS days_since_last_order,
       customer_items.number_of_orders       AS number_of_orders,
       customer_items.number_of_items        AS number_of_order_items,
       customer_items.revenue_lifetime       AS revenue_lifetime,
       customer_items.total_freight_value    AS total_freight_value
FROM ec_tmp.customer
         LEFT JOIN ec_tmp.zip_code USING (zip_code)
         LEFT JOIN customer_items USING (customer_id)
         LEFT JOIN customer_orders USING (customer_id);

SELECT util.add_index('ec_dim_next', 'customer', column_names := ARRAY ['zip_code_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_customer()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'customer', 'ec_dim_next', 'zip_code');
SELECT util.add_fk('ec_dim_next', 'customer', 'first_order_fk', 'ec_dim_next', 'order');
SELECT util.add_fk('ec_dim_next', 'customer', 'last_order_fk', 'ec_dim_next', 'order');
$$
    LANGUAGE sql;
