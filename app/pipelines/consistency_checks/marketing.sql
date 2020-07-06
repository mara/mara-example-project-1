SELECT util.assert_almost_equal(
               'The total amount of lifetime revenue should be equal among seller and deal dim tables',
               0.001,
               'SELECT sum(revenue_lifetime) FROM m_dim.deal',
               'SELECT sum(seller.revenue_lifetime) ' ||
               'FROM ec_dim.seller ' ||
               'INNER JOIN m_dim.deal ON seller_id = seller_fk'
           );

SELECT util.assert_almost_equal(
               'The total amount of lifetime revenue should be equal among order_item and deal dim tables',
               0.001,
               'SELECT sum(revenue_lifetime) FROM m_dim.deal',
               'SELECT sum(revenue) ' ||
               'FROM ec_dim.order_item ' ||
               'INNER JOIN m_dim.deal USING (seller_fk)'
           );

SELECT util.assert_equal(
               'The total number of items should be equal among order_item and deal dim tables',
               'SELECT sum(number_of_order_items) FROM m_dim.deal',
               'SELECT count(*) ' ||
               'FROM ec_dim.order_item ' ||
               'INNER JOIN m_dim.deal USING (seller_fk)'
           );
