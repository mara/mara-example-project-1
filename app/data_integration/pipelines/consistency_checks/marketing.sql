SELECT util.assert_equal(
           'The number of marketing qualified leads entries should be preserved in marketing-funnel dim table',
           'SELECT count(*) FROM m_tmp.marketing_qualified_lead',
           'SELECT count(*) FROM m_dim.marketing_funnel');

SELECT util.assert_almost_equal(
           'The total amount of lifetime revenue should be equal among seller and marketing_funnel dim tables',
           0.001,
           'SELECT sum(revenue_lifetime) FROM m_dim.marketing_funnel',
           'SELECT sum(seller.revenue_lifetime) ' ||
           'FROM ec_dim.seller ' ||
           'INNER JOIN m_dim.closed_deal ON seller_id = seller_fk'
         );

SELECT util.assert_almost_equal(
           'The total amount of lifetime revenue should be equal among order_item and marketing_funnel dim tables',
           0.001,
           'SELECT sum(revenue_lifetime) FROM m_dim.marketing_funnel',
           'SELECT sum(revenue) ' ||
           'FROM ec_dim.order_item ' ||
           'INNER JOIN m_dim.closed_deal USING (seller_fk)'
         );

SELECT util.assert_equal(
           'The total number of items should be equal among order_item and marketing_funnel dim tables',
           'SELECT sum(number_of_order_items) FROM m_dim.marketing_funnel',
           'SELECT count(*) ' ||
           'FROM ec_dim.order_item ' ||
           'INNER JOIN m_dim.closed_deal USING (seller_fk)'
         );
