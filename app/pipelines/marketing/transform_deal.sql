DROP TABLE IF EXISTS m_dim_next.closed_deal CASCADE;
CREATE TABLE m_dim_next.closed_deal
(

  closed_deal_id                TEXT                              NOT NULL PRIMARY KEY, -- The Marketing Qualified Lead id of the closed deal as PK
  marketing_qualified_lead_fk   TEXT                              NOT NULL,             --Marketing Qualified Lead id
  seller_fk                     TEXT,                                                   --Seller id
  sdr_id                        TEXT                              NOT NULL,             --Sales Development Representative id
  sr_id                         TEXT                              NOT NULL,             --Sales Representative

  won_date                      TIMESTAMP WITH TIME ZONE,                               --Date the deal was closed.

  business_segment              m_dim_next.BUSINESS_SEGMENT       NOT NULL,             --Lead business segment. Informed on contact.
  lead_type                     m_dim_next.LEAD_TYPE              NOT NULL,             --Lead type. Informed on contact.
  lead_behaviour_profile        m_dim_next.LEAD_BEHAVIOUR_PROFILE NOT NULL,             --Lead behaviour profile. SDR identify it on contact
  has_company                   m_dim_next.HAS_COMPANY,                                 --Does the lead have a company (formal documentation)?
  has_gtin                      m_dim_next.HAS_GTIN,                                    --Does the lead have Global Trade Item Number (barcode) for his products?
  average_stock                 m_dim_next.AVERAGE_STOCK          NOT NULL,             --Lead declared average stock. Informed on contact.
  business_type                 m_dim_next.BUSINESS_TYPE          NOT NULL,             --Type of business (reseller/manufacturer etc.)

  declared_product_catalog_size DOUBLE PRECISION,                                       --Lead declared catalog size. Informed on contact.
  declared_monthly_revenue      DOUBLE PRECISION                                       --Lead declared estimated monthly revenue. Informed on contact.

--   number_of_orders              INTEGER,
--   number_of_order_items         INTEGER,
--   number_of_deliveries          INTEGER,
--   number_of_customers           INTEGER,
--   revenue_lifetime              DOUBLE PRECISION,
--   total_freight_value           DOUBLE PRECISION
);

INSERT INTO m_dim_next.closed_deal
SELECT closed_deal_id                                           AS closed_deal_id,
       marketing_qualified_lead_id                              AS marketing_qualified_lead_fk,
       seller.seller_id                                         AS seller_fk,
       sdr_id                                                   AS sdr_id,
       sr_id                                                    AS sr_id,

       won_date                                                 AS won_date,

       COALESCE(business_segment,
                'Unknown') :: m_dim_next.BUSINESS_SEGMENT       AS business_segment,
       COALESCE(lead_type,
                'Unknown') :: m_dim_next.LEAD_TYPE              AS lead_type,
       COALESCE(lead_behaviour_profile,
                'Unknown') :: m_dim_next.LEAD_BEHAVIOUR_PROFILE AS lead_behaviour_profile,

       CASE
         WHEN has_company IS TRUE
           THEN 'Has company'
         WHEN has_company IS FALSE
           THEN 'Has not company'
         ELSE 'Unknown' END :: m_dim_next.HAS_COMPANY           AS has_company,

       CASE
         WHEN has_gtin IS TRUE
           THEN 'Has GTIN'
         WHEN has_gtin IS FALSE
           THEN 'Has not GTIN'
         ELSE 'Unknown' END :: m_dim_next.HAS_GTIN              AS has_gtin,

       COALESCE(average_stock,
                'Unknown') :: m_dim_next.AVERAGE_STOCK          AS average_stock,
       COALESCE(business_type,
                'Unknown') :: m_dim_next.BUSINESS_TYPE          AS business_type,

       coalesce(declared_product_catalog_size, 0)               AS declared_product_catalog_size,
       coalesce(declared_monthly_revenue, 0)                    AS declared_monthly_revenue

--        seller.number_of_orders,
--        seller.number_of_order_items,
--        seller.number_of_deliveries,
--        seller.number_of_customers,
--        seller.revenue_lifetime,
--        seller.total_freight_value
FROM m_tmp.closed_deal
     LEFT JOIN ec_dim.seller using (seller_id);

SELECT util.add_index('m_dim_next', 'closed_deal',
                      column_names := ARRAY ['marketing_qualified_lead_fk', 'seller_fk']);

CREATE OR REPLACE FUNCTION m_tmp.constrain_deal()
  RETURNS VOID AS
$$
SELECT util.add_fk('m_dim_next', 'closed_deal', 'm_dim_next', 'marketing_qualified_lead');
SELECT util.add_fk('m_dim_next', 'closed_deal', 'ec_dim', 'seller');
$$
  LANGUAGE SQL;
