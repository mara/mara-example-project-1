SELECT util.create_enum(
           'ec_dim_next.STATUS',
           (SELECT array_agg(DISTINCT status) FROM ec_tmp.order));

DROP TABLE IF EXISTS ec_dim_next.order CASCADE;

CREATE TABLE ec_dim_next.order
(
  order_id                TEXT NOT NULL PRIMARY KEY, --unique identifier of the order.
  customer_fk             TEXT NOT NULL,             --key to the customer table. Each order has a unique customer_id.

  status                  ec_dim_next.STATUS,        --Reference to the order status (delivered, shipped, etc).

  purchase_date      TIMESTAMP WITH TIME ZONE,  --Shows the purchase timestamp.
  approved_at_date             TIMESTAMP WITH TIME ZONE,  --Shows the payment approval timestamp.
  delivered_carrier_date  TIMESTAMP WITH TIME ZONE,  --Shows the order posting timestamp. When it was handled to the logistic partner.
  delivered_customer_date TIMESTAMP WITH TIME ZONE,  --Shows the actual order delivery date to the customer.
  estimated_delivery_date TIMESTAMP WITH TIME ZONE,  --Shows the estimated delivery date that was informed to customer at the purchase moment.

  number_of_items         INTEGER,
  total_price             DOUBLE PRECISION,
  total_freight_value     DOUBLE PRECISION
);

WITH items AS (
  SELECT order_id,
         count(*)           AS number_of_items,
         sum(price)         AS total_price,
         sum(freight_value) AS total_freight_value
  FROM ec_tmp.order_item
  GROUP BY order_id
)

INSERT
INTO ec_dim_next.order
SELECT order_id,
       customer_id                AS customer_fk,

       status::ec_dim_next.STATUS AS status,

       purchase_date,
       approved_at_date,
       delivered_carrier_date,
       delivered_customer_date,
       estimated_delivery_date,

       items.number_of_items      AS number_of_items,
       items.total_price          AS total_price,
       items.total_freight_value  AS total_freight_value
FROM ec_tmp.order
     LEFT JOIN items USING (order_id);

SELECT util.add_index('ec_dim_next', 'order', column_names := ARRAY ['customer_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_orders()
  RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'order', 'ec_dim_next', 'customer');
$$
  LANGUAGE SQL;
