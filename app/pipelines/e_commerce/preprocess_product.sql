DROP TABLE IF EXISTS ec_tmp.product CASCADE;

CREATE TABLE ec_tmp.product
(
    product_id       TEXT NOT NULL, --unique product identifier

    product_category TEXT,          --root category of product

    weight           INTEGER,       --product weight measured in grams.
    length           INTEGER,       --product length measured in centimeters.
    height           INTEGER,       --product height measured in centimeters.
    width            INTEGER,       --product width measured in centimeters.
    number_of_photos INTEGER        --number of product published photos
);

INSERT INTO ec_tmp.product
SELECT product_id,

       coalesce(coalesce(product_category_name_translation.product_category_name_english,
                         product.product_category_name), 'Unknown') AS product_category,

       weight_g                                                     AS weight,
       length_cm                                                    AS length,
       height_cm                                                    AS height,
       width_cm                                                     AS width,
       photos_quantity                                              AS number_of_photos
FROM ec_data.product
         LEFT JOIN ec_data.product_category_name_translation USING (product_category_name);

SELECT util.add_index('ec_tmp', 'product', column_names := ARRAY ['product_id']);

ANALYZE ec_tmp.product;

SELECT util.create_enum(
               'ec_dim_next.PRODUCT_CATEGORY',
               (SELECT array_agg(DISTINCT product_category)
                FROM ec_tmp.product
                WHERE product_category IS NOT NULL));
