SELECT util.create_enum('m_dim_next.LANDING_PAGE',
                        (SELECT array_agg(DISTINCT landing_page_id) FROM m_tmp.marketing_qualified_lead));

SELECT util.create_enum('m_dim_next.ORIGIN',
                        (SELECT array_agg(DISTINCT origin) FROM m_tmp.marketing_qualified_lead));

SELECT util.create_enum('m_dim_next.BUSINESS_SEGMENT',
                        (SELECT array_agg(DISTINCT coalesce(business_segment, 'Unknown')) FROM m_tmp.closed_deal));

SELECT util.create_enum('m_dim_next.LEAD_TYPE',
                        (SELECT array_agg(DISTINCT coalesce(lead_type, 'Unknown')) FROM m_tmp.closed_deal));

SELECT util.create_enum('m_dim_next.LEAD_BEHAVIOUR_PROFILE',
                        (SELECT array_agg(DISTINCT coalesce(lead_behaviour_profile, 'Unknown'))
                         FROM m_tmp.closed_deal));

SELECT util.create_enum('m_dim_next.HAS_COMPANY',
                        ARRAY ['Has company', 'Has not company', 'Unknown']);

SELECT util.create_enum('m_dim_next.HAS_GTIN',
                        ARRAY ['Has GTIN', 'Has not GTIN', 'Unknown']);

SELECT util.create_enum('m_dim_next.IS_CLOSED_DEAL',
                        ARRAY ['Is closed deal', 'Is not closed deal']);

SELECT util.create_enum('m_dim_next.AVERAGE_STOCK',
                        (SELECT array_agg(DISTINCT coalesce(average_stock, 'Unknown')) FROM m_tmp.closed_deal));

SELECT util.create_enum('m_dim_next.BUSINESS_TYPE',
                        (SELECT array_agg(DISTINCT coalesce(business_type, 'Unknown')) FROM m_tmp.closed_deal));
