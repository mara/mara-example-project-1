--This is the core table. From each order you might find all other information.
DROP TABLE IF EXISTS ec_data.order CASCADE;
CREATE TABLE ec_data.order
(
    order_id                      TEXT,                     --unique identifier of the order.
    customer_id                   TEXT,                     --key to the customer table. Each order has a unique customer_id.
    order_status                  TEXT,                     --Reference to the order status (delivered, shipped, etc).
    order_purchase_timestamp      TIMESTAMP WITH TIME ZONE,                --Shows the purchase timestamp.
    order_approved_at             TIMESTAMP WITH TIME ZONE, --Shows the payment approval timestamp.
    order_delivered_carrier_date  TIMESTAMP WITH TIME ZONE, --Shows the order posting timestamp. When it was handled to the logistic partner.
    order_delivered_customer_date TIMESTAMP WITH TIME ZONE, --Shows the actual order delivery date to the customer.
    order_estimated_delivery_date TIMESTAMP WITH TIME ZONE  --Shows the estimated delivery date that was informed to customer at the purchase moment.
);