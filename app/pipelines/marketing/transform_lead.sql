DROP TABLE IF EXISTS m_dim_next.lead CASCADE;
CREATE TABLE m_dim_next.lead
(
    lead_id                       TEXT                              NOT NULL PRIMARY KEY, --Marketing Qualified Lead id
    seller_fk                     TEXT,                                                   --Seller id
    sdr_id                        TEXT,                                                   --Sales Development Representative id
    sr_id                         TEXT,                                                   --Sales Representative

    deal_date                     TIMESTAMP WITH TIME ZONE,                               --Date the deal was closed.

    business_segment              m_dim_next.BUSINESS_SEGMENT       NOT NULL,             --Lead business segment. Informed on contact.
    lead_type                     m_dim_next.LEAD_TYPE              NOT NULL,             --Lead type. Informed on contact.
    lead_behaviour_profile        m_dim_next.LEAD_BEHAVIOUR_PROFILE NOT NULL,             --Lead behaviour profile. SDR identify it on contact
    average_stock                 m_dim_next.AVERAGE_STOCK          NOT NULL,             --Lead declared average stock. Informed on contact.
    business_type                 m_dim_next.BUSINESS_TYPE          NOT NULL,             --Type of business (reseller/manufacturer etc.)

    declared_product_catalog_size DOUBLE PRECISION,                                       --Lead declared catalog size. Informed on contact.
    declared_monthly_revenue      DOUBLE PRECISION,                                       --Lead declared estimated monthly revenue. Informed on contact.

    is_closed_deal                m_dim_next.IS_CLOSED_DEAL         NOT NULL,

    first_contact_date            TIMESTAMP WITH TIME ZONE          NOT NULL,             --Date of the first contact solicitation.
    landing_page_id               m_dim_next.LANDING_PAGE           NOT NULL,             --Landing page id where the lead was acquired
    advertising_channel           m_dim_next.ADVERTISING_CHANNEL    NOT NULL,             --Type of media where the lead was acquired

    number_of_orders_lifetime     INTEGER,
    revenue_lifetime              DOUBLE PRECISION,
    days_to_closing_deal          INTEGER
);

INSERT INTO m_dim_next.lead
SELECT lead_id                                                        AS lead_id,
       seller.seller_id                                               AS seller_fk,
       sdr_id                                                         AS sdr_id,
       sr_id                                                          AS sr_id,

       deal_date                                                      AS deal_date,

       COALESCE(business_segment,
                'Unknown') :: m_dim_next.BUSINESS_SEGMENT             AS business_segment,
       COALESCE(lead_type,
                'Unknown') :: m_dim_next.LEAD_TYPE                    AS lead_type,
       COALESCE(lead_behaviour_profile,
                'Unknown') :: m_dim_next.LEAD_BEHAVIOUR_PROFILE       AS lead_behaviour_profile,

       COALESCE(average_stock,
                'Unknown') :: m_dim_next.AVERAGE_STOCK                AS average_stock,
       COALESCE(business_type,
                'Unknown') :: m_dim_next.BUSINESS_TYPE                AS business_type,

       coalesce(declared_product_catalog_size, 0)                     AS declared_product_catalog_size,
       coalesce(declared_monthly_revenue, 0)                          AS declared_monthly_revenue,

       CASE
           WHEN lead.deal_date IS NOT NULL
               THEN 'Is closed deal'
           ELSE 'Is not closed deal' END :: m_dim_next.IS_CLOSED_DEAL AS is_closed_deal,

       first_contact_date                                             AS first_contact_date,
       landing_page_id :: m_dim_next.LANDING_PAGE                     AS landing_page_id,
       advertising_channel :: m_dim_next.ADVERTISING_CHANNEL          AS advertising_channel,

       seller.number_of_orders_lifetime                               AS number_of_orders_lifetime,
       seller.revenue_lifetime                                        AS revenue_lifetime,
       days_to_closing_deal                                           AS days_to_closing_deal
FROM m_tmp.lead
         LEFT JOIN ec_dim.seller USING (seller_id);

SELECT util.add_index('m_dim_next', 'lead',
                      column_names := ARRAY ['seller_fk']);

CREATE OR REPLACE FUNCTION m_tmp.constrain_lead()
    RETURNS VOID AS
$$
SELECT util.add_fk('m_dim_next', 'lead', 'ec_dim', 'seller');
$$
    LANGUAGE sql;
