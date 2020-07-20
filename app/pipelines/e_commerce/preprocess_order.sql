DROP TABLE IF EXISTS ec_tmp.order CASCADE;

CREATE TABLE ec_tmp.order
(
    order_id               TEXT NOT NULL,            --unique identifier of the order.
    customer_id            TEXT NOT NULL,            --key to the customer table. Each order has a unique customer_id.

    order_status           TEXT,                     --Reference to the order status (delivered, shipped, etc).

    order_date             TIMESTAMP WITH TIME ZONE, --Shows the purchase timestamp.
    payment_approval_date  TIMESTAMP WITH TIME ZONE, --Shows the payment approval timestamp.
    delivery_date          TIMESTAMP WITH TIME ZONE, --Shows the actual order delivery date to the customer.

    delivery_time_in_days  INTEGER,                  -- date-diff of order_date, delivery_date
    days_since_first_order INTEGER
);

WITH order_with_unique_customer_id AS (
    SELECT "order".order_id,
--            "order".customer_id                                                  AS customer_id_to_order,
           customer.customer_unique_id                                          AS customer_id,
           order_status                                                         AS order_status,

           order_purchase_timestamp                                             AS order_date,
           order_approved_at                                                    AS payment_approval_date,
           order_delivered_customer_date                                        AS delivery_date,
           order_delivered_customer_date::DATE - order_purchase_timestamp::DATE AS days_of_delivery
    FROM ec_data.order
             LEFT JOIN ec_data.customer USING (customer_id)
)

INSERT
INTO ec_tmp."order"
SELECT order_id,
       customer_id                                        AS customer_id,

       order_status                                       AS order_status,

       order_date                                         AS order_date,
       payment_approval_date                              AS payment_approval_date,
       delivery_date                                      AS delivery_date,
       days_of_delivery                                   AS days_of_delivery,
       order_date::DATE - customer.first_order_date::DATE AS days_since_first_order
FROM order_with_unique_customer_id
         LEFT JOIN ec_tmp.customer USING (customer_id);

SELECT util.add_index('ec_tmp', 'order', column_names := ARRAY ['order_id', 'customer_id']);
