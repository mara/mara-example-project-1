--After a lead fills in a form at a landing page, a filter is made to select the ones that are qualified to sell their products at Olist.
--They are the Marketing Qualified Leads (MQLs).
DROP TABLE IF EXISTS m_data.marketing_qualified_lead CASCADE;
CREATE TABLE m_data.marketing_qualified_lead
(
    mql_id             TEXT,                     --Marketing Qualified Lead id
    first_contact_date TIMESTAMP WITH TIME ZONE, --Date of the first contact solicitation.
    landing_page_id    TEXT,                     --Landing page id where the lead was acquired
    origin             TEXT                      --Type of media where the lead was acquired
);