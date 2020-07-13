-- Closed deals: After a qualified lead fills in a form at a landing page he is contacted by a Sales Development Representative.
-- At this step some information is checked and more information about the lead is gathered.

DROP TABLE IF EXISTS m_tmp.lead CASCADE;
CREATE TABLE m_tmp.lead
(
    lead_id                       TEXT                     NOT NULL, --Marketing Qualified Lead id
    seller_id                     TEXT,                              --Seller id
    sdr_id                        TEXT,                              --Sales Development Representative id
    sr_id                         TEXT,                              --Sales Representative

    deal_date                     TIMESTAMP WITH TIME ZONE,          --Date the deal was closed.
    business_segment              TEXT,                              --Lead business segment. Informed on contact.
    lead_type                     TEXT,                              --Lead type. Informed on contact.
    lead_behaviour_profile        TEXT,                              --Lead behaviour profile. SDR identify it on contact
    has_company                   BOOLEAN,                           --Does the lead have a company (formal documentation)?
    has_gtin                      BOOLEAN,                           --Does the lead have Global Trade Item Number (barcode) for his products?
    average_stock                 TEXT,                              --Lead declared average stock. Informed on contact.
    business_type                 TEXT,                              --Type of business (reseller/manufacturer etc.)

    declared_product_catalog_size DOUBLE PRECISION,                  --Lead declared catalog size. Informed on contact.
    declared_monthly_revenue      DOUBLE PRECISION,                  --Lead declared estimated monthly revenue. Informed on contact.

    first_contact_date            TIMESTAMP WITH TIME ZONE NOT NULL, --Date of the first contact solicitation.
    landing_page_id               TEXT                     NOT NULL, --Landing page id where the lead was acquired
    advertising_channel           TEXT                     NOT NULL, --Type of media where the lead was acquired
    days_to_closing_deal          INTEGER
);

INSERT INTO m_tmp.lead
SELECT mql_id                                       AS lead_id,
       seller_id,
       sdr_id,
       sr_id,

       won_date                                     AS deal_date,
       business_segment                             AS business_segment,
       lead_type                                    AS lead_type,
       lead_behaviour_profile                       AS lead_behaviour_profile,
       has_company::BOOLEAN                         AS has_company,
       has_gtin::BOOLEAN                            AS has_gtin,
       average_stock                                AS average_stock,
       business_type                                AS business_type,
       declared_product_catalog_size,
       declared_monthly_revenue,
       first_contact_date::TIMESTAMP WITH TIME ZONE AS first_contact_date,
       landing_page_id,
       COALESCE(origin, 'Unknown')                  AS advertising_channel,
       DATE_PART('day', won_datet -
                        first_contact_date)         AS days_to_closing_deal
FROM m_data.marketing_qualified_lead
         LEFT JOIN m_data.closed_deal USING (mql_id);

SELECT util.add_index('m_tmp', 'lead',
                      column_names := ARRAY ['lead_id', 'seller_id']);
