DROP TABLE IF EXISTS ec_dim_next.order_item CASCADE;

CREATE TABLE ec_dim_next.order_item
(
    order_item_id     TEXT             NOT NULL PRIMARY KEY, -- sequential number identifying number of items included in the same order.
    order_fk          TEXT             NOT NULL,             -- order unique identifier
    customer_fk       TEXT             NOT NULL,             -- Unique identifier of a customer
    product_fk        TEXT             NOT NULL,             -- product unique identifier
    seller_fk         TEXT             NOT NULL,             -- seller unique identifier
    is_first_order_id TEXT,

    product_revenue   DOUBLE PRECISION NOT NULL,             -- item price
    shipping_revenue  DOUBLE PRECISION NOT NULL              -- item freight value item (if an order has more than one item the freight value is split between items)
);

INSERT INTO ec_dim_next.order_item
SELECT order_item_id,
       order_id    AS order_fk,
       customer_id AS customer_fk,
       product_id  AS product_fk,
       seller_id   AS seller_fk,

       is_first_order_id,

       product_revenue,
       shipping_revenue
FROM ec_tmp.order_item;

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
