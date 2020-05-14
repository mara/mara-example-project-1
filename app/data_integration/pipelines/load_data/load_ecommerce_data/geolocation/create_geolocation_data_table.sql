--This table has information Brazilian zip codes and its lat/lng coordinates.
--Use it to plot maps and find distances between sellers and customers.
DROP TABLE IF EXISTS ec_data.geolocation CASCADE;
CREATE TABLE ec_data.geolocation
(
    zip_code_prefix TEXT,             --first 5 digits of zip code
    latitude        DOUBLE PRECISION, --latitude
    longitude       DOUBLE PRECISION, --longitude
    city            TEXT,             --city name
    state           TEXT              --state
);