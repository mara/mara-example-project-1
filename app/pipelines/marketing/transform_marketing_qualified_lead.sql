DROP TABLE IF EXISTS m_dim_next.marketing_qualified_lead CASCADE;
CREATE TABLE m_dim_next.marketing_qualified_lead
(

    marketing_qualified_lead_id TEXT                      NOT NULL PRIMARY KEY, --Marketing Qualified Lead id
    is_closed_deal              m_dim_next.IS_CLOSED_DEAL NOT NULL,

    first_contact_date          TIMESTAMP WITH TIME ZONE  NOT NULL,             --Date of the first contact solicitation.
    landing_page_id             m_dim_next.LANDING_PAGE   NOT NULL,             --Landing page id where the lead was acquired
    origin                      m_dim_next.ORIGIN         NOT NULL              --Type of media where the lead was acquired

);

INSERT INTO m_dim_next.marketing_qualified_lead
SELECT mql.marketing_qualified_lead_id                                AS marketing_qualified_lead_id,
       CASE
           WHEN deal.deal_date IS NOT NULL
               THEN 'Is closed deal'
           ELSE 'Is not closed deal' END :: m_dim_next.IS_CLOSED_DEAL AS is_closed_deal,

       first_contact_date                                             AS first_contact_date,
       landing_page_id :: m_dim_next.LANDING_PAGE                     AS landing_page_id,
       origin :: m_dim_next.ORIGIN                                    AS origin
FROM m_tmp.marketing_qualified_lead mql
         LEFT JOIN m_tmp.deal ON mql.marketing_qualified_lead_id = deal.marketing_qualified_lead_id

