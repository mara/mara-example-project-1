DROP TABLE IF EXISTS ec_tmp.customer CASCADE;

CREATE TABLE ec_tmp.customer
(
    customer_id            TEXT NOT NULL, -- Unique identifier of a customer
    zip_code               TEXT NOT NULL, -- First five digits of customer zip code
    first_order_id         TEXT,
    first_order_date       TIMESTAMP WITH TIME ZONE,
    last_order_id          TEXT,
    city                   TEXT,          --customer city name
    state                  TEXT,          --customer state

    days_since_first_order INTEGER,
    days_since_last_order  INTEGER

);

WITH customer_orders AS (
    SELECT DISTINCT customer.customer_unique_id,
                    first_value(zip_code_prefix)
                    OVER (PARTITION BY customer_unique_id
                        ORDER BY order_purchase_timestamp DESC)                   AS zip_code,
                    first_value(initcap(city))
                    OVER (PARTITION BY customer_unique_id
                        ORDER BY order_purchase_timestamp DESC)                   AS city,
                    first_value(state)
                    OVER (PARTITION BY customer_unique_id
                        ORDER BY order_purchase_timestamp DESC)                   AS state,
                    first_value(order_id)
                    OVER (PARTITION BY customer.customer_unique_id
                        ORDER BY "order".order_purchase_timestamp ASC)            AS first_order_id,
                    first_value(order_purchase_timestamp)
                    OVER (PARTITION BY customer.customer_unique_id
                        ORDER BY "order".order_purchase_timestamp ASC)            AS first_order_date,
                    first_value(order_id)
                    OVER (PARTITION BY customer.customer_unique_id
                        ORDER BY "order".order_purchase_timestamp DESC)           AS last_order_id,
                    now() :: DATE
                        - MIN("order".order_purchase_timestamp)
                          OVER (PARTITION BY customer.customer_unique_id) :: DATE AS days_since_first_order,
                    now() :: DATE
                        - MAX("order".order_purchase_timestamp)
                          OVER (PARTITION BY customer.customer_unique_id) :: DATE AS days_since_last_order
    FROM ec_data.order
             LEFT JOIN ec_data.customer USING (customer_id)
)

-- Customers get different ids for different orders -> Deduplication on customer_unique_id
-- Keep the last order's customer data across distinct customer_unique_id
-- If there is no order data (this is because the order data was not sampled), keep the first_value
INSERT
INTO ec_tmp.customer
SELECT DISTINCT customer.customer_unique_id            AS customer_id,
                first_value(coalesce(customer_orders.zip_code, customer.zip_code_prefix))
                OVER (PARTITION BY customer_unique_id) AS zip_code,
                customer_orders.first_order_id         AS first_order_id,
                customer_orders.first_order_date       AS first_order_date,
                customer_orders.last_order_id          AS last_order_id,
                first_value(coalesce(customer_orders.city, customer.city))
                OVER (PARTITION BY customer_unique_id) AS city,
                first_value(coalesce(customer_orders.state, customer.state))
                OVER (PARTITION BY customer_unique_id) AS state,
                customer_orders.days_since_first_order AS days_since_first_order,
                customer_orders.days_since_last_order  AS days_since_last_order

FROM ec_data.customer
         LEFT JOIN customer_orders USING (customer_unique_id);

SELECT util.add_index('ec_tmp', 'customer', column_names := ARRAY ['customer_id']);
