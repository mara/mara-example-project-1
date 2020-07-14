SELECT util.create_enum(
               'ec_dim_next.STATUS',
               (SELECT array_agg(DISTINCT status) FROM ec_tmp.order));

DROP TABLE IF EXISTS ec_dim_next.order CASCADE;

CREATE TABLE ec_dim_next.order
(
    order_id               TEXT NOT NULL PRIMARY KEY, --unique identifier of the order.
    customer_fk            TEXT NOT NULL,             --key to the customer table. Each order has a unique customer_id.

    status                 ec_dim_next.STATUS,        --Reference to the order status (delivered, shipped, etc).

    order_date             TIMESTAMP WITH TIME ZONE,  --Shows the purchase timestamp.
    payment_approval_date  TIMESTAMP WITH TIME ZONE,  --Shows the payment approval timestamp.
    delivery_date          TIMESTAMP WITH TIME ZONE,  --Shows the actual order delivery date to the customer.

    delivery_time_in_days  INTEGER,                   -- date-diff of order_date, delivery_date
    days_since_first_order INTEGER
);

WITH customer_first_order AS (
    SELECT customer.customer_id,
           "order".order_date AS first_order_date
    FROM ec_dim.customer
             LEFT JOIN ec_tmp."order"
                       ON customer.first_order_fk = "order".order_id
)

INSERT
INTO ec_dim_next.order
SELECT order_id,
       customer_id                               AS customer_fk,

       status::ec_dim_next.STATUS                AS status,

       order_date,
       payment_approval_date,
       delivery_date,
       delivery_time_in_days,
       order_date::DATE - first_order_date::DATE AS days_since_first_order

FROM ec_tmp.order
         LEFT JOIN customer_first_order USING (customer_id);

SELECT util.add_index('ec_dim_next', 'order', column_names := ARRAY ['customer_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_orders()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'order', 'ec_dim_next', 'customer');
$$
    LANGUAGE sql;
