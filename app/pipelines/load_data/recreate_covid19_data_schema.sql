DROP SCHEMA IF EXISTS covid19_data CASCADE;
CREATE SCHEMA covid19_data;

SELECT util.create_chunking_functions('covid19_data');