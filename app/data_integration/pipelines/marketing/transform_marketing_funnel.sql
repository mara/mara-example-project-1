DROP TABLE IF EXISTS m_dim_next.marketing_funnel CASCADE;
CREATE TABLE m_dim_next.marketing_funnel
(
  marketing_qualified_lead_fk   TEXT                      NOT NULL PRIMARY KEY, --Marketing Qualified Lead id
  closed_deal_fk                TEXT,                                           --Closed deal MQL id

  is_closed_deal                m_dim_next.IS_CLOSED_DEAL NOT NULL,

  declared_product_catalog_size DOUBLE PRECISION,                               --Lead declared catalog size. Informed on contact.
  declared_monthly_revenue      DOUBLE PRECISION,                               --Lead declared estimated monthly revenue. Informed on contact.

  number_of_orders              INTEGER,
  number_of_order_items         INTEGER,
  number_of_deliveries          INTEGER,
  number_of_customers           INTEGER,
  revenue_lifetime              DOUBLE PRECISION,
  total_freight_value           DOUBLE PRECISION
);

INSERT INTO m_dim_next.marketing_funnel
SELECT mql.marketing_qualified_lead_id                              AS marketing_qualified_lead_fk,
       deal.closed_deal_id                                          AS closed_deal_id,

       CASE
         WHEN deal.won_date IS NOT NULL
           THEN 'Is closed deal'
         ELSE 'Is not closed deal' END :: m_dim_next.IS_CLOSED_DEAL AS is_closed_deal,

       coalesce(deal.declared_product_catalog_size, 0)              AS declared_product_catalog_size,
       coalesce(deal.declared_monthly_revenue, 0)                   AS declared_monthly_revenue,

       deal.number_of_orders,
       deal.number_of_order_items,
       deal.number_of_deliveries,
       deal.number_of_customers,
       deal.revenue_lifetime,
       deal.total_freight_value
FROM m_dim_next.marketing_qualified_lead mql
     LEFT JOIN m_dim_next.closed_deal deal ON marketing_qualified_lead_id = marketing_qualified_lead_fk;

SELECT util.add_index('m_dim_next', 'marketing_funnel',
                      column_names := ARRAY ['marketing_qualified_lead_fk', 'closed_deal_fk']);

CREATE OR REPLACE FUNCTION m_tmp.constrain_marketing_funnel()
  RETURNS VOID AS
$$
SELECT util.add_fk('m_dim_next', 'marketing_funnel', 'm_dim_next', 'marketing_qualified_lead');
SELECT util.add_fk('m_dim_next', 'marketing_funnel', 'm_dim_next', 'closed_deal');
$$
  LANGUAGE SQL;
