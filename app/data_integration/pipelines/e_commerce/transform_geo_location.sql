SELECT util.create_enum(
           'ec_dim_next.ZIP_CODE_PREFIX',
           (SELECT array_agg(DISTINCT zip_code_prefix) FROM ec_tmp.geo_location));

SELECT util.create_enum(
           'ec_dim_next.CITY',
           (SELECT array_agg(DISTINCT city) FROM ec_tmp.geo_location));

SELECT util.create_enum(
           'ec_dim_next.STATE',
           (SELECT array_agg(DISTINCT state) FROM ec_tmp.geo_location));

DROP TABLE IF EXISTS ec_dim_next.geo_location CASCADE;

CREATE TABLE ec_dim_next.geo_location
(
  geo_location_id INTEGER                     NOT NULL PRIMARY KEY, -- Unique integer representation of the zip_code_prefix

  zip_code_prefix ec_dim_next.ZIP_CODE_PREFIX NOT NULL,             -- First 5 digits of zip code
  latitude        DOUBLE PRECISION,
  longitude       DOUBLE PRECISION,
  city            ec_dim_next.CITY            NOT NULL,
  state           ec_dim_next.STATE           NOT NULL
);

INSERT INTO ec_dim_next.geo_location
SELECT geo_location_id,
       zip_code_prefix::ec_dim_next.ZIP_CODE_PREFIX AS zip_code_prefix,
       latitude                                     AS latitude,
       longitude                                    AS longitude,
       city::ec_dim_next.CITY                       AS city,
       state::ec_dim_next.STATE                     AS state
FROM ec_tmp.geo_location;

