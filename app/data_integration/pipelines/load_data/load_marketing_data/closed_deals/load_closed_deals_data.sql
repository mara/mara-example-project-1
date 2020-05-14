SELECT mql_id,
       seller_id,
       sdr_id,
       sr_id,
       won_date,
       business_segment,
       lead_type,
       lead_behaviour_profile,
       has_company,
       has_gtin,
       average_stock,
       business_type,
       declared_product_catalog_size,
       declared_monthly_revenue
FROM marketing.closed_deals
WHERE won_date >= to_date('@@first-date@@', 'YYYY-MM-DD')
