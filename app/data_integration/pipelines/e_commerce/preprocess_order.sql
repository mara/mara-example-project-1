DROP TABLE IF EXISTS ec_tmp.order CASCADE;

CREATE TABLE ec_tmp.order
(
  order_id                TEXT NOT NULL,            --unique identifier of the order.
  customer_id             TEXT NOT NULL,            --key to the customer table. Each order has a unique customer_id.

  status                  TEXT,                     --Reference to the order status (delivered, shipped, etc).

  purchase_date           TIMESTAMP WITH TIME ZONE, --Shows the purchase timestamp.
  approved_at_date        TIMESTAMP WITH TIME ZONE, --Shows the payment approval timestamp.
  delivered_carrier_date  TIMESTAMP WITH TIME ZONE, --Shows the order posting timestamp. When it was handled to the logistic partner.
  delivered_customer_date TIMESTAMP WITH TIME ZONE, --Shows the actual order delivery date to the customer.
  estimated_delivery_date TIMESTAMP WITH TIME ZONE  --Shows the estimated delivery date that was informed to customer at the purchase moment.
);

INSERT INTO ec_tmp.order
SELECT order_id,
       customers.customer_unique_id  AS customer_id,

       order_status                  AS status,

       order_purchase_timestamp      AS purchase_date,
       order_approved_at             AS approved_at_date,
       order_delivered_carrier_date  AS delivered_carrier_date,
       order_delivered_customer_date AS delivered_customer_date,
       order_estimated_delivery_date AS estimated_delivery_date
FROM ec_data.orders
     LEFT JOIN ec_data.customers ON orders.customer_id = customers.customer_id;

SELECT util.add_index('ec_tmp', 'order', column_names := ARRAY ['order_id', 'customer_id']);
