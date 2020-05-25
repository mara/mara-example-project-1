DROP TABLE IF EXISTS m_dim_next.marketing_funnel CASCADE;
CREATE TABLE m_dim_next.marketing_funnel
(
  mql_id                        TEXT                              NOT NULL PRIMARY KEY, --Marketing Qualified Lead id
  closed_deal_id                TEXT,                                                   --Closed deal MQL id
  seller_fk                     TEXT,
  sdr_id                        TEXT,                                                   --Sales Development Representative id
  sr_id                         TEXT,                                                   --Sales Representative

  first_contact_date            DATE                              NOT NULL,             --Date of the first contact solicitation.
  landing_page_id               m_dim_next.LANDING_PAGE           NOT NULL,             --Landing page id where the lead was acquired
  origin                        m_dim_next.ORIGIN                 NOT NULL,             --Type of media where the lead was acquired

  is_closed_deal                m_dim_next.IS_CLOSED_DEAL         NOT NULL,
  won_date                      TIMESTAMP WITH TIME ZONE,                               --Date the deal was closed.

  business_segment              m_dim_next.BUSINESS_SEGMENT       NOT NULL,             --Lead business segment. Informed on contact.
  lead_type                     m_dim_next.LEAD_TYPE              NOT NULL,             --Lead type. Informed on contact.
  lead_behaviour_profile        m_dim_next.LEAD_BEHAVIOUR_PROFILE NOT NULL,             --Lead behaviour profile. SDR identify it on contact
  has_company                   m_dim_next.HAS_COMPANY,                                 --Does the lead have a company (formal documentation)?
  has_gtin                      m_dim_next.HAS_GTIN,                                    --Does the lead have Global Trade Item Number (barcode) for his products?
  average_stock                 m_dim_next.AVERAGE_STOCK          NOT NULL,             --Lead declared average stock. Informed on contact.
  business_type                 m_dim_next.BUSINESS_TYPE          NOT NULL,             --Type of business (reseller/manufacturer etc.)

  declared_product_catalog_size DOUBLE PRECISION,                                       --Lead declared catalog size. Informed on contact.
  declared_monthly_revenue      DOUBLE PRECISION,                                       --Lead declared estimated monthly revenue. Informed on contact.

  number_of_orders              INTEGER,
  number_of_order_items         INTEGER,
  number_of_deliveries          INTEGER,
  number_of_customers           INTEGER,
  revenue_lifetime              DOUBLE PRECISION,
  total_freight_value           DOUBLE PRECISION
);

INSERT INTO m_dim_next.marketing_funnel
SELECT mql.mql_id                                                                            AS mql_id,
       deal.closed_deal_id                                                                   AS closed_deal_id,
       seller.seller_id                                                                      AS seller_fk,
       deal.sdr_id                                                                           AS sdr_id,
       deal.sr_id                                                                            AS sr_id,

       mql.first_contact_date                                                                AS first_contact_date,
       mql.landing_page_id :: m_dim_next.LANDING_PAGE                                        AS landing_page_id,
       mql.origin :: m_dim_next.ORIGIN                                                       AS origin,

       CASE
         WHEN deal.won_date IS NOT NULL
           THEN 'Is closed deal'
         ELSE 'Is not closed deal' END :: m_dim_next.IS_CLOSED_DEAL                          AS is_closed_deal,
       deal.won_date                                                                         AS won_date,

       COALESCE(deal.business_segment, 'Unknown') :: m_dim_next.BUSINESS_SEGMENT             AS business_segment,
       COALESCE(deal.lead_type, 'Unknown') :: m_dim_next.LEAD_TYPE                           AS lead_type,
       COALESCE(deal.lead_behaviour_profile, 'Unknown') :: m_dim_next.LEAD_BEHAVIOUR_PROFILE AS lead_behaviour_profile,

       CASE
         WHEN deal.has_company IS TRUE
           THEN 'Has company'
         WHEN deal.has_company IS FALSE
           THEN 'Has not company'
         ELSE 'Unknown' END :: m_dim_next.HAS_COMPANY                                        AS has_company,

       CASE
         WHEN deal.has_gtin IS TRUE
           THEN 'Has GTIN'
         WHEN deal.has_gtin IS FALSE
           THEN 'Has not GTIN'
         ELSE 'Unknown' END :: m_dim_next.HAS_GTIN                                           AS has_gtin,

       COALESCE(deal.average_stock, 'Unknown') :: m_dim_next.AVERAGE_STOCK                   AS average_stock,
       COALESCE(deal.business_type, 'Unknown') :: m_dim_next.BUSINESS_TYPE                   AS business_type,

       coalesce(deal.declared_product_catalog_size, 0)                                       AS declared_product_catalog_size,
       coalesce(deal.declared_monthly_revenue, 0)                                            AS declared_monthly_revenue,

       seller.number_of_orders,
       seller.number_of_order_items,
       seller.number_of_deliveries,
       seller.number_of_customers,
       seller.revenue_lifetime,
       seller.total_freight_value
FROM m_tmp.marketing_qualified_lead mql
     LEFT JOIN m_tmp.closed_deal deal using (mql_id)
     LEFT JOIN ec_dim.seller using (seller_id);

SELECT util.add_index('m_dim_next', 'marketing_funnel',
                      column_names := ARRAY ['mql_id', 'closed_deal_id', 'seller_fk']);

CREATE OR REPLACE FUNCTION m_tmp.constrain_marketing_funnel()
  RETURNS VOID AS
$$
SELECT util.add_fk('m_dim_next', 'marketing_funnel', 'ec_dim', 'seller');
$$
  LANGUAGE SQL;
