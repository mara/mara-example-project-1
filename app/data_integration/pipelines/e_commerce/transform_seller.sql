DROP TABLE IF EXISTS ec_dim_next.seller CASCADE;

CREATE TABLE ec_dim_next.seller
(
  seller_id                      TEXT    NOT NULL PRIMARY KEY, -- seller unique identifier
  geo_location_fk                INTEGER NOT NULL,             -- integer representation of a zip_code_prefix
  first_order_fk                 TEXT,
  last_order_fk                  TEXT,

  first_order_purchase_date TIMESTAMP WITH TIME ZONE,
  last_order_purchase_date  TIMESTAMP WITH TIME ZONE,
  days_since_last_order          INTEGER,

  number_of_orders               INTEGER,
  number_of_order_items          INTEGER,
  number_of_customers            INTEGER,
  lifetime_amount                DOUBLE PRECISION,
  total_freight_value            DOUBLE PRECISION
);

WITH seller_items   AS (
  SELECT seller_id,
         count(*)                    AS number_of_items,
         count(distinct order_id)    AS number_of_orders,
         count(distinct customer_id) AS number_of_customers,
         sum(price)                  AS lifetime_amount,
         sum(freight_value)          AS total_freight_value
  FROM ec_tmp.order_item
  GROUP BY seller_id
)
    , seller_orders AS (
  SELECT DISTINCT seller_id,
                  first_value(order_id)
                              over (partition by seller_id
                                order by _purchase_date asc)  AS first_order_id,
                  first_value(_purchase_date)
                              over (partition by seller_id
                                order by _purchase_date asc)  AS first_order_purchase_date,

                  first_value(order_id)
                              over (partition by seller_id
                                order by _purchase_date desc) AS last_order_id,

                  first_value(_purchase_date)
                              over (partition by seller_id
                                order by _purchase_date desc) AS last_order_purchase_date,
                  now() :: DATE
                    - MAX(_purchase_date)
                          over (partition by seller_id) :: DATE    AS days_since_last_order
  FROM ec_tmp.order_item
)

INSERT
INTO ec_dim_next.seller
SELECT seller_id,
       geo_location.geo_location_id                 AS geo_location_fk,

       seller_orders.first_order_id                 AS first_order_fk,
       seller_orders.last_order_id                  AS last_order_fk,

       seller_orders.first_order_purchase_date AS first_order_purchase_date,
       seller_orders.last_order_purchase_date  AS last_order_purchase_date,
       seller_orders.days_since_last_order          AS days_since_last_order,

       seller_items.number_of_orders                AS number_of_orders,
       seller_items.number_of_items                 AS number_of_order_items,
       seller_items.number_of_customers             AS number_of_customers,
       seller_items.lifetime_amount                 AS lifetime_amount,
       seller_items.total_freight_value             AS total_freight_value
FROM ec_tmp.seller
     LEFT JOIN ec_tmp.geo_location USING (zip_code_prefix)
     LEFT JOIN seller_items USING (seller_id)
     LEFT JOIN seller_orders USING (seller_id);

SELECT util.add_index('ec_dim_next', 'seller', column_names := ARRAY ['seller_id', 'geo_location_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_sellers()
  RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'seller', 'ec_dim_next', 'geo_location');
SELECT util.add_fk('ec_dim_next', 'seller', 'first_order_fk', 'ec_dim_next', 'order');
SELECT util.add_fk('ec_dim_next', 'seller', 'last_order_fk', 'ec_dim_next', 'order');
$$
  LANGUAGE SQL;
