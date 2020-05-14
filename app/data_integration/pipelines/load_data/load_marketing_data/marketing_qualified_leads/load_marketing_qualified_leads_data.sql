SELECT mql_id,
       first_contact_date,
       landing_page_id,
       origin
FROM marketing.marketing_qualified_leads
WHERE first_contact_date >= to_date('@@first-date@@', 'YYYY-MM-DD')
