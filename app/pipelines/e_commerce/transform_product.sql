DROP TABLE IF EXISTS ec_dim_next.product CASCADE;

CREATE TABLE ec_dim_next.product
(
    product_id       TEXT NOT NULL PRIMARY KEY,    --unique product identifier

    product_category ec_dim_next.PRODUCT_CATEGORY, --root category of product, in English.

    weight           INTEGER,                      --product weight measured in grams.
    length           INTEGER,                      --product length measured in centimeters.
    height           INTEGER,                      --product height measured in centimeters.
    width            INTEGER,                      --product width measured in centimeters.
    number_of_photos INTEGER,                      --number of product published photos

    product_revenue  DOUBLE PRECISION
);

WITH product_items AS (
    SELECT product_id,
           sum(product_revenue) AS product_revenue
    FROM ec_tmp.order_item
             LEFT JOIN ec_tmp.order USING (order_id)
    GROUP BY product_id
)

INSERT
INTO ec_dim_next.product
SELECT product_id,

       product_category::ec_dim_next.PRODUCT_CATEGORY AS category,

       weight,
       length,
       height,
       width,
       number_of_photos,

       product_items.product_revenue                  AS product_revenue
FROM ec_tmp.product
         LEFT JOIN product_items USING (product_id);

