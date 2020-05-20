-- MQLs: Leads that are qualified to sell their products at Olist, after selection based on a landing_page form
DROP TABLE IF EXISTS m_tmp.marketing_qualified_lead CASCADE;

CREATE TABLE m_tmp.marketing_qualified_lead
(
  mql_id             TEXT NOT NULL, --Marketing Qualified Lead id
  first_contact_date DATE NOT NULL, --Date of the first contact solicitation.
  landing_page_id    TEXT NOT NULL, --Landing page id where the lead was acquired
  origin             TEXT NOT NULL  --Type of media where the lead was acquired
);

INSERT INTO m_tmp.marketing_qualified_lead
SELECT mql_id,
       first_contact_date,
       landing_page_id,
       COALESCE(origin, 'Unknown') AS origin
FROM m_data.marketing_qualified_leads;

SELECT util.add_index('m_tmp', 'marketing_qualified_lead', column_names := ARRAY ['mql_id']);
