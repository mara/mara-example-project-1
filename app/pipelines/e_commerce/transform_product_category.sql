DROP TABLE IF EXISTS ec_dim_next.product_category CASCADE;

CREATE TABLE ec_dim_next.product_category
(
    product_category_id         INTEGER PRIMARY KEY, --unique ID of the product category
    product_category            TEXT,                --category name in English
    product_category_portuguese TEXT                 --category name in Portuguese
);

INSERT INTO ec_dim_next.product_category
SELECT product_category_id,
       product_category,
       product_category_portuguese
FROM ec_tmp.product_category


