DROP TABLE IF EXISTS ec_tmp.order_item CASCADE;

CREATE TABLE ec_tmp.order_item
(
  order_item_id       TEXT             NOT NULL, --sequential number identifying number of items included in the same order.
  order_id            TEXT             NOT NULL, --order unique identifier
  customer_id         TEXT             NOT NULL, -- Unique identifier of a customer
  product_id          TEXT             NOT NULL, --product unique identifier
  seller_id           TEXT             NOT NULL, --seller unique identifier

  shipping_limit_date TIMESTAMP WITH TIME ZONE,  --Shows the seller shipping limit date for handling the order over to the logistic partner.
  revenue             DOUBLE PRECISION NOT NULL, --item price
  freight_value       DOUBLE PRECISION NOT NULL  --item freight value item (if an order has more than one item the freight value is split between items)
);

INSERT INTO ec_tmp.order_item
SELECT order_id || '_' || order_item_id AS order_item_id, -- create a unique order_item_id
       order_id,
       "order".customer_id              AS customer_id,
       product_id,
       seller_id,

       shipping_limit_date,
       price                            AS revenue,
       freight_value
FROM ec_data.order_items
     LEFT JOIN ec_tmp.order USING (order_id)
     -- Leave out order-items without order information
WHERE "order".order_id IS NOT NULL;

SELECT util.add_index('ec_tmp', 'order_item',
                      column_names := ARRAY ['order_item_id', 'order_id', 'product_id', 'seller_id']);
