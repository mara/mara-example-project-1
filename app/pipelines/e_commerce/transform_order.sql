SELECT util.create_enum(
               'ec_dim_next.ORDER_STATUS',
               (SELECT array_agg(DISTINCT order_status) FROM ec_tmp.order));

DROP TABLE IF EXISTS ec_dim_next.order CASCADE;

CREATE TABLE ec_dim_next.order
(
    order_id               TEXT NOT NULL PRIMARY KEY, --unique identifier of the order.
    customer_fk            TEXT NOT NULL,             --key to the customer table. Each order has a unique customer_id.

    order_status           ec_dim_next.ORDER_STATUS,  --Reference to the order status (delivered, shipped, etc).

    order_date             TIMESTAMP WITH TIME ZONE,  --Shows the purchase timestamp.
    payment_approval_date  TIMESTAMP WITH TIME ZONE,  --Shows the payment approval timestamp.
    delivery_date          TIMESTAMP WITH TIME ZONE,  --Shows the actual order delivery date to the customer.

    delivery_time_in_days  INTEGER,                   -- date-diff of order_date, delivery_date
    days_since_first_order INTEGER
);

INSERT
INTO ec_dim_next.order
SELECT order_id,
       customer_id                      AS customer_fk,

       order_status::ec_dim_next.ORDER_STATUS AS order_status,

       order_date,
       payment_approval_date,
       delivery_date,
       delivery_time_in_days,
       days_since_first_order

FROM ec_tmp.order;

SELECT util.add_index('ec_dim_next', 'order', column_names := ARRAY ['customer_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_orders()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'order', 'ec_dim_next', 'customer');
$$
    LANGUAGE sql;
