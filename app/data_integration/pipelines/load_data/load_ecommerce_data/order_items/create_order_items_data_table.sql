--This table includes data about the items purchased within each order.
DROP TABLE IF EXISTS ec_data.order_items CASCADE;
CREATE TABLE ec_data.order_items
(
    order_id            TEXT,                     --order unique identifier
    order_item_id       INTEGER,                  --sequential number identifying number of items included in the same order.
    product_id          TEXT,                     --product unique identifier
    seller_id           TEXT,                     --seller unique identifier
    shipping_limit_date TIMESTAMP WITH TIME ZONE, --Shows the seller shipping limit date for handling the order over to the logistic partner.
    price               DOUBLE PRECISION,         --item price
    freight_value       DOUBLE PRECISION          --item freight value item (if an order has more than one item the freight value is split between items)
);