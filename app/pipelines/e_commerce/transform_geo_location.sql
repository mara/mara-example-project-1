DROP TABLE IF EXISTS ec_dim_next.geo_location CASCADE;

CREATE TABLE ec_dim_next.geo_location
(
    geo_location_id  INTEGER NOT NULL PRIMARY KEY, -- Unique integer representation of the zip_code_prefix

    zip_code_prefix  TEXT    NOT NULL,             -- First 5 digits of zip code
    zip_code_digit_1 TEXT    NOT NULL,
    zip_code_digit_2 TEXT    NOT NULL,
    zip_code_digit_3 TEXT    NOT NULL,
    zip_code_digit_4 TEXT    NOT NULL,
    latitude         DOUBLE PRECISION,
    longitude        DOUBLE PRECISION,
    city             TEXT    NOT NULL,
    state            TEXT    NOT NULL
);

INSERT INTO ec_dim_next.geo_location
SELECT geo_location_id,
       zip_code_prefix  AS zip_code_prefix,
       zip_code_digit_1 AS zip_code_digit_1,
       zip_code_digit_2 AS zip_code_digit_2,
       zip_code_digit_3 AS zip_code_digit_3,
       zip_code_digit_4 AS zip_code_digit_4,
       latitude         AS latitude,
       longitude        AS longitude,
       city             AS city,
       state            AS state
FROM ec_tmp.geo_location;

