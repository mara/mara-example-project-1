DROP TABLE IF EXISTS ec_tmp.seller CASCADE;

CREATE TABLE ec_tmp.seller
(
    seller_id      TEXT NOT NULL, -- seller unique identifier
    zip_code       TEXT NOT NULL, -- integer representation of a zip_code_prefix
    first_order_id TEXT,
    city           TEXT,
    state          TEXT
);

WITH seller_orders AS (
    SELECT DISTINCT order_item.seller_id,
                    first_value("order".order_id)
                    OVER (PARTITION BY order_item.seller_id
                        ORDER BY "order".order_purchase_timestamp ASC) AS first_order_id
    FROM ec_data.order_item
             LEFT JOIN ec_data.order USING (order_id)
)

INSERT
INTO ec_tmp.seller
SELECT seller_id       AS seller_id,
       zip_code_prefix AS zip_code,
       first_order_id  AS first_order_id,
       initcap(city)   AS city,
       state           AS state
FROM ec_data.seller
         LEFT JOIN seller_orders USING (seller_id);

SELECT util.add_index('ec_tmp', 'seller', column_names := ARRAY ['seller_id']);

ANALYZE ec_tmp.seller;