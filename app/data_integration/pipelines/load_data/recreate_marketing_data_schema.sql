DROP SCHEMA IF EXISTS m_data CASCADE;
CREATE SCHEMA m_data;

SELECT util.create_chunking_functions('m_data');