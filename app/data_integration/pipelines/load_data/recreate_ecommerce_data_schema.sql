DROP SCHEMA IF EXISTS ec_data CASCADE;
CREATE SCHEMA ec_data;

SELECT util.create_chunking_functions('ec_data');