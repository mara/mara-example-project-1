DROP TABLE IF EXISTS ec_dim_next.product CASCADE;

CREATE TABLE ec_dim_next.product
(
    product_id                TEXT NOT NULL PRIMARY KEY,    --unique product identifier

    product_category          ec_dim_next.PRODUCT_CATEGORY, --root category of product, in Portuguese.

    number_of_photos          INTEGER,                      --number of product published photos
    weight                    INTEGER,                      --product weight measured in grams.
    length                    INTEGER,                      --product length measured in centimeters.
    height                    INTEGER,                      --product height measured in centimeters.
    width                     INTEGER,                      --product width measured in centimeters.

    number_of_order_items     INTEGER,
    product_revenue           DOUBLE PRECISION,
    avg_delivery_time_in_days DOUBLE PRECISION
);

WITH product_items AS (
    SELECT product_id,
           count(*)                           AS number_of_items,
           sum(product_revenue)               AS product_revenue,
           avg("order".delivery_time_in_days) AS avg_delivery_time_in_days
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
    GROUP BY product_id
)

INSERT
INTO ec_dim_next.product
SELECT product_id,

       product_category::ec_dim_next.PRODUCT_CATEGORY AS category,

       number_of_photos,
       weight,
       length,
       height,
       width,

       product_items.number_of_items                  AS number_of_order_items,
       product_items.product_revenue                  AS product_revenue,
       product_items.avg_delivery_time_in_days        AS avg_delivery_time_in_days
FROM ec_tmp.product
         LEFT JOIN product_items USING (product_id);

