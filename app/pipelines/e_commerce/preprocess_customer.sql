DROP TABLE IF EXISTS ec_tmp.customer CASCADE;

CREATE TABLE ec_tmp.customer
(
    customer_id TEXT NOT NULL, -- Unique identifier of a customer
    zip_code    TEXT NOT NULL, -- First five digits of customer zip code
    city        TEXT,
    state       TEXT
);

-- Customers get different ids for different orders -> Deduplication on customer_unique_id
-- Keep the last order's customer data across distinct customer_unique_id
INSERT INTO ec_tmp.customer
SELECT DISTINCT customer_unique_id                          AS customer_id,
                first_value(zip_code_prefix)
                OVER (PARTITION BY customer_unique_id
                    ORDER BY order_purchase_timestamp DESC) AS zip_code,
                first_value(initcap(city))
                OVER (PARTITION BY customer_unique_id
                    ORDER BY order_purchase_timestamp DESC) AS city,
                first_value(state)
                OVER (PARTITION BY customer_unique_id
                    ORDER BY order_purchase_timestamp DESC) AS state
FROM ec_data.customer
         LEFT JOIN ec_data.order USING (customer_id);

SELECT util.add_index('ec_tmp', 'customer', column_names := ARRAY ['customer_id']);
