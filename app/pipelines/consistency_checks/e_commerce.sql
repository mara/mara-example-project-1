SELECT util.assert_equal(
               'The number of customer entries should be the same in tmp and dim schemas',
               'SELECT count(*) FROM ec_tmp.customer',
               'SELECT count(*) FROM ec_dim.customer');

SELECT util.assert_equal(
               'The number of seller entries should be the same in tmp and dim schemas',
               'SELECT count(*) FROM ec_tmp.seller',
               'SELECT count(*) FROM ec_dim.seller');

SELECT util.assert_equal(
               'The number of order-item entries should be the same in tmp and dim schemas',
               'SELECT count(*) FROM ec_tmp.order_item',
               'SELECT count(*) FROM ec_dim.order_item');

SELECT util.assert_equal(
               'The number of distinct customer orders should be the same in customer and order dim tables',
               'SELECT sum(number_of_orders) FROM ec_dim.customer',
               'SELECT count(distinct order_fk) FROM ec_dim.order_item');

SELECT util.assert_equal(
               'The number of distinct customer orders should be the same in customer and order dim tables',
               'SELECT sum(number_of_orders) FROM ec_dim.customer',
               'SELECT count(distinct order_fk) FROM ec_dim.order_item');

SELECT util.assert_equal(
               'The number of distinct items should be the same in order and order_item dim tables',
               'SELECT sum(number_of_items) FROM ec_dim."order"',
               'SELECT count(*) FROM ec_dim.order_item');

SELECT util.assert_not_found(
               'There should not be any orders with order_date greater than payment_approval_date',
               'select * from ec_dim."order" where order_date::DATE > payment_approval_date::DATE;');

SELECT util.assert_almost_equal(
               'The total amount of lifetime revenue should be equal among customer and order-item dim tables',
               0.001,
               'SELECT sum(revenue_lifetime) FROM ec_dim.customer',
               'SELECT sum(product_revenue) FROM ec_dim.order_item'
           );

SELECT util.assert_almost_equal(
               'The total amount of lifetime revenue should be equal among seller and order-item dim tables',
               0.001,
               'SELECT sum(revenue_lifetime) FROM ec_dim.seller',
               'SELECT sum(product_revenue) FROM ec_dim.order_item'
           );
