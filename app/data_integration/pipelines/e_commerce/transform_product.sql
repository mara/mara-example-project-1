SELECT util.create_enum(
           'ec_dim_next.PRODUCT_CATEGORY',
           (SELECT array_agg(DISTINCT product_category)
            FROM ec_tmp.product
            WHERE product_category IS NOT NULL));

DROP TABLE IF EXISTS ec_dim_next.product CASCADE;

CREATE TABLE ec_dim_next.product
(
  product_id            TEXT NOT NULL PRIMARY KEY,    --unique product identifier

  product_category      ec_dim_next.PRODUCT_CATEGORY, --root category of product, in Portuguese.

  photos_quantity       INTEGER,                      --number of product published photos
  weight_g              INTEGER,                      --product weight measured in grams.
  length_cm             INTEGER,                      --product length measured in centimeters.
  height_cm             INTEGER,                      --product height measured in centimeters.
  width_cm              INTEGER,                      --product width measured in centimeters.

  number_of_orders      INTEGER,
  number_of_order_items INTEGER,
  number_of_customers   INTEGER,
  lifetime_amount       DOUBLE PRECISION,
  total_freight_value   DOUBLE PRECISION
);

WITH product_items AS (
  SELECT product_id,
         count(*)                    AS number_of_items,
         count(distinct order_id)    AS number_of_orders,
         count(distinct customer_id) AS number_of_customers,
         sum(price)                  AS lifetime_amount,
         sum(freight_value)          AS total_freight_value
  FROM ec_tmp.order_item
  GROUP BY product_id
)

INSERT
INTO ec_dim_next.product
SELECT product_id,

       product_category::ec_dim_next.PRODUCT_CATEGORY AS product_category,

       photos_quantity,
       weight_g,
       length_cm,
       height_cm,
       width_cm,

       product_items.number_of_orders                 AS number_of_orders,
       product_items.number_of_items                  AS number_of_order_items,
       product_items.number_of_customers              AS number_of_customers,
       product_items.lifetime_amount                  AS lifetime_amount,
       product_items.total_freight_value              AS total_freight_value
FROM ec_tmp.product
     LEFT JOIN product_items USING (product_id);

SELECT util.add_index('ec_dim_next', 'product', column_names := ARRAY ['product_id']);

