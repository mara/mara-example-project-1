-- Closed deals: After a qualified lead fills in a form at a landing page he is contacted by a Sales Development Representative.
-- At this step some information is checked and more information about the lead is gathered.

DROP TABLE IF EXISTS m_tmp.closed_deal CASCADE;
CREATE TABLE m_tmp.closed_deal
(
  closed_deal_id                TEXT NOT NULL,            -- The Marketing Qualified Lead id of the closed deal as PK
  mql_id                        TEXT NOT NULL,            --Marketing Qualified Lead id
  seller_id                     TEXT NOT NULL,            --Seller id
  sdr_id                        TEXT NOT NULL,            --Sales Development Representative id
  sr_id                         TEXT NOT NULL,            --Sales Representative

  won_date                      TIMESTAMP WITH TIME ZONE, --Date the deal was closed.
  business_segment              TEXT,                     --Lead business segment. Informed on contact.
  lead_type                     TEXT,                     --Lead type. Informed on contact.
  lead_behaviour_profile        TEXT,                     --Lead behaviour profile. SDR identify it on contact
  has_company                   BOOLEAN,                  --Does the lead have a company (formal documentation)?
  has_gtin                      BOOLEAN,                  --Does the lead have Global Trade Item Number (barcode) for his products?
  average_stock                 TEXT,                     --Lead declared average stock. Informed on contact.
  business_type                 TEXT,                     --Type of business (reseller/manufacturer etc.)

  declared_product_catalog_size DOUBLE PRECISION,         --Lead declared catalog size. Informed on contact.
  declared_monthly_revenue      DOUBLE PRECISION          --Lead declared estimated monthly revenue. Informed on contact.
);

INSERT INTO m_tmp.closed_deal
SELECT mql_id                 AS closed_deal_id,
       mql_id,
       seller_id,
       sdr_id,
       sr_id,

       won_date,
       business_segment       AS business_segment,
       lead_type              AS lead_type,
       lead_behaviour_profile AS lead_behaviour_profile,
       has_company::BOOLEAN   AS has_company,
       has_gtin::BOOLEAN      AS has_gtin,
       average_stock          AS average_stock,
       business_type          AS business_type,
       declared_product_catalog_size,
       declared_monthly_revenue
FROM m_data.closed_deals;

SELECT util.add_index('m_tmp', 'closed_deal', column_names := ARRAY ['closed_deal_id', 'mql_id', 'seller_id']);
