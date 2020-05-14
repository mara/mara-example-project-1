--This table includes data about the orders payment options.
DROP TABLE IF EXISTS ec_data.order_payments CASCADE;
CREATE TABLE ec_data.order_payments
(
    order_id             TEXT,            --unique identifier of an order.
    payment_sequential   INTEGER,         --a customer may pay an order with more than one payment method. If he does so, a sequence will be created to
    payment_type         TEXT,            --method of payment chosen by the customer.
    payment_installments INTEGER,         --number of installments chosen by the customer.
    payment_value        DOUBLE PRECISION --transaction value.
);