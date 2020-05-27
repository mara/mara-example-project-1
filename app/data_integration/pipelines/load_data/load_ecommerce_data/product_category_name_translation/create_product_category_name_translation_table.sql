--Translates the product_category_name to english.
DROP TABLE IF EXISTS ec_data.product_category_name_translation CASCADE;
CREATE TABLE ec_data.product_category_name_translation
(
    product_category_name         TEXT, --category name in Portuguese
    product_category_name_english TEXT  --category name in English
);