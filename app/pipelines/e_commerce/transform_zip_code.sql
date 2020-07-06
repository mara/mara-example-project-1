DROP TABLE IF EXISTS ec_dim_next.zip_code CASCADE;

CREATE TABLE ec_dim_next.zip_code
(
    zip_code_id      INTEGER NOT NULL PRIMARY KEY, -- Unique integer representation of the zip_code_prefix

    zip_code         TEXT    NOT NULL,             -- First 5 digits of zip code
    latitude         DOUBLE PRECISION,
    longitude        DOUBLE PRECISION,
    city             TEXT    NOT NULL,
    state            TEXT    NOT NULL
);

INSERT INTO ec_dim_next.zip_code
SELECT zip_code_id,
       zip_code         AS zip_code,
       latitude         AS latitude,
       longitude        AS longitude,
       city             AS city,
       state            AS state
FROM ec_tmp.zip_code;

