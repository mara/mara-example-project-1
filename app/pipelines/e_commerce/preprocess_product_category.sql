DROP TABLE IF EXISTS ec_tmp.product_category CASCADE;

CREATE TABLE ec_tmp.product_category
(
    product_category_id         INTEGER, --unique ID of the product category
    product_category            TEXT,    --category name in English
    product_category_portuguese TEXT     --category name in Portuguese
);

CREATE SEQUENCE IF NOT EXISTS ec_tmp.product_category_id;

WITH all_product_catagories AS (
    SELECT DISTINCT product_category_name
    FROM ec_data.product
    UNION
    SELECT product_category_name
    FROM ec_data.product_category_name_translation
)

INSERT
INTO ec_tmp.product_category
SELECT nextval('ec_tmp.product_category_id')                          AS product_category_id,
       coalesce(product_category_name_english, product_category_name) AS product_category,
       product_category_name                                          AS product_category_portuguese
FROM all_product_catagories
         LEFT JOIN ec_data.product_category_name_translation
                   USING (product_category_name);

SELECT util.add_index('ec_tmp', 'product_category', column_names := ARRAY ['product_category_id']);
