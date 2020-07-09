DROP TABLE IF EXISTS ec_dim_next.order_item CASCADE;

CREATE TABLE ec_dim_next.order_item
(
    order_item_id       TEXT             NOT NULL PRIMARY KEY, -- sequential number identifying number of items included in the same order.
    order_fk            TEXT             NOT NULL,             -- order unique identifier
    customer_fk         TEXT             NOT NULL,             -- Unique identifier of a customer
    product_fk          TEXT             NOT NULL,             -- product unique identifier
    seller_fk           TEXT             NOT NULL,             -- seller unique identifier
    first_order_id      TEXT,

    shipping_limit_date TIMESTAMP WITH TIME ZONE,              -- Shows the seller shipping limit date for handling the order over to the logistic partner.
    product_revenue     DOUBLE PRECISION NOT NULL,             -- item price
    shipping_revenue    DOUBLE PRECISION NOT NULL              -- item freight value item (if an order has more than one item the freight value is split between items)
);

INSERT INTO ec_dim_next.order_item
SELECT order_item_id,
       order_id               AS order_fk,
       order_item.customer_id AS customer_fk,
       product_id             AS product_fk,
       seller_id              AS seller_fk,

       CASE
           WHEN
                           first_value(order_id)
                           OVER (PARTITION BY "order".customer_id
                               ORDER BY "order".order_date ASC) = order_id THEN
                       first_value(order_id)
                       OVER (PARTITION BY "order".customer_id
                           ORDER BY "order".order_date ASC)
           ELSE NULL END      AS first_order_id,

       shipping_limit_date,
       product_revenue,
       shipping_revenue
FROM ec_tmp.order_item
         LEFT JOIN ec_tmp.order USING (order_id);

SELECT util.add_index('ec_dim_next', 'order_item',
                      column_names := ARRAY ['order_fk', 'customer_fk', 'product_fk', 'seller_fk']);

CREATE OR REPLACE FUNCTION ec_tmp.constrain_order_item()
    RETURNS VOID AS
$$
SELECT util.add_fk('ec_dim_next', 'order_item', 'ec_dim_next', 'order');
SELECT util.add_fk('ec_dim_next', 'order_item', 'ec_dim_next', 'customer');
SELECT util.add_fk('ec_dim_next', 'order_item', 'ec_dim_next', 'product');
SELECT util.add_fk('ec_dim_next', 'order_item', 'ec_dim_next', 'seller');
$$
    LANGUAGE sql;
