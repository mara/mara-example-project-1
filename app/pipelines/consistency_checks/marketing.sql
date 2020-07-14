SELECT util.assert_almost_equal(
               'The total amount of lifetime revenue should be equal among seller and lead dim tables',
               0.001,
               'SELECT sum(lifetime_sales) FROM m_dim.lead',
               'SELECT sum(seller.lifetime_sales) ' ||
               'FROM ec_dim.seller ' ||
               'INNER JOIN m_dim.lead ON seller_id = seller_fk'
           );

SELECT util.assert_almost_equal(
               'The total amount of lifetime revenue should be equal among order_item and lead dim tables',
               0.001,
               'SELECT sum(lifetime_sales) FROM m_dim.lead',
               'SELECT sum(order_item.product_revenue)+sum(order_item.shipping_revenue) ' ||
               'FROM ec_dim.order_item ' ||
               'INNER JOIN m_dim.lead USING (seller_fk)'
           );

SELECT util.assert_equal(
               'The total number orders should be equal among order_item and lead dim tables',
               'SELECT sum(lifetime_number_of_orders) FROM m_dim.lead',
               'SELECT sum(seller.lifetime_number_of_orders) ' ||
               'FROM ec_dim.seller ' ||
               'INNER JOIN m_dim.lead on seller.seller_id = lead.seller_fk'
           );
