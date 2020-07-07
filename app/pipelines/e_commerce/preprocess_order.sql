DROP TABLE IF EXISTS ec_tmp.order CASCADE;

CREATE TABLE ec_tmp.order
(
    order_id                      TEXT NOT NULL,            --unique identifier of the order.
    customer_id                   TEXT NOT NULL,            --key to the customer table. Each order has a unique customer_id.

    status                        TEXT,                     --Reference to the order status (delivered, shipped, etc).

    order_date                    TIMESTAMP WITH TIME ZONE, --Shows the purchase timestamp.
    payment_approval_date         TIMESTAMP WITH TIME ZONE, --Shows the payment approval timestamp.
    delivery_date                 TIMESTAMP WITH TIME ZONE, --Shows the actual order delivery date to the customer.

    payment_approval_time_in_days INTEGER,                  -- date-diff of order_date, order_approved_at
    delivery_time_in_days         INTEGER                   -- date-diff of order_date, delivery_date
);

INSERT INTO ec_tmp.order
SELECT order_id,
       customer.customer_unique_id                AS customer_id,

       order_status                               AS status,

       order_purchase_timestamp                   AS order_date,
       order_approved_at                          AS payment_approval_date,
       order_delivered_customer_date              AS delivery_date,
       DATE_PART('day', order_approved_at -
                        order_purchase_timestamp) AS payment_approval_time_in_days,

       DATE_PART('day', order_delivered_customer_date -
                        order_purchase_timestamp) AS days_of_delivery
FROM ec_data.order
         LEFT JOIN ec_data.customer USING (customer_id);

SELECT util.add_index('ec_tmp', 'order', column_names := ARRAY ['order_id', 'customer_id']);
