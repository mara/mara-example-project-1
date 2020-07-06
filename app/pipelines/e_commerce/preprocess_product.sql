DROP TABLE IF EXISTS ec_tmp.product CASCADE;

CREATE TABLE ec_tmp.product
(
    product_id       TEXT NOT NULL, --unique product identifier

    product_category TEXT,          --root category of product

    number_of_photos INTEGER,       --number of product published photos
    weight           INTEGER,       --product weight measured in grams.
    length           INTEGER,       --product length measured in centimeters.
    height           INTEGER,       --product height measured in centimeters.
    width            INTEGER        --product width measured in centimeters.
);

INSERT INTO ec_tmp.product
SELECT product_id,

       coalesce(coalesce(product_category_name_translation.product_category_name_english,
                         product.product_category_name), 'Unknown') AS product_category,

       photos_quantity                                              AS number_of_photos,
       weight_g                                                     AS weight,
       length_cm                                                    AS length,
       height_cm                                                    AS height,
       width_cm                                                     AS width
FROM ec_data.product
         LEFT JOIN ec_data.product_category_name_translation USING (product_category_name);

SELECT util.add_index('ec_tmp', 'product', column_names := ARRAY ['product_id']);
