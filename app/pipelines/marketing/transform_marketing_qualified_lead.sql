DROP TABLE IF EXISTS m_dim_next.marketing_qualified_lead CASCADE;
CREATE TABLE m_dim_next.marketing_qualified_lead
(

  marketing_qualified_lead_id TEXT                     NOT NULL PRIMARY KEY, --Marketing Qualified Lead id

  first_contact_date          TIMESTAMP WITH TIME ZONE NOT NULL,             --Date of the first contact solicitation.
  landing_page_id             m_dim_next.LANDING_PAGE  NOT NULL,             --Landing page id where the lead was acquired
  origin                      m_dim_next.ORIGIN        NOT NULL              --Type of media where the lead was acquired

);

INSERT INTO m_dim_next.marketing_qualified_lead
SELECT marketing_qualified_lead_id                AS marketing_qualified_lead_id,

       first_contact_date                         AS first_contact_date,
       landing_page_id :: m_dim_next.LANDING_PAGE AS landing_page_id,
       origin :: m_dim_next.ORIGIN                AS origin
FROM m_tmp.marketing_qualified_lead;

SELECT util.add_index('m_dim_next', 'marketing_qualified_lead',
                      column_names := ARRAY ['marketing_qualified_lead_id']);
