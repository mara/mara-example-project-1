DROP TABLE IF EXISTS ec_tmp.zip_code CASCADE;

CREATE TABLE ec_tmp.zip_code
(
    zip_code_id      INTEGER NOT NULL, -- Unique integer representation of the zip_code_prefix

    zip_code         TEXT    NOT NULL, -- First 5 digits of zip code
    zip_code_digit_1 TEXT    NOT NULL,
    zip_code_digit_2 TEXT    NOT NULL,
    zip_code_digit_3 TEXT    NOT NULL,
    zip_code_digit_4 TEXT    NOT NULL,
    latitude         DOUBLE PRECISION,
    longitude        DOUBLE PRECISION,
    city             TEXT    NOT NULL,
    state            TEXT    NOT NULL
);

WITH zip_codes AS (
    SELECT zip_code_prefix,
           latitude      AS latitude,
           longitude     AS longitude,
           initcap(city) AS city,
           state         AS state
    FROM ec_data.geolocation
    UNION ALL
    SELECT zip_code,
           NULL AS latitude,
           NULL AS longitude,
           city,
           state
    FROM ec_tmp.seller
    UNION ALL
    SELECT zip_code,
           NULL AS latitude,
           NULL AS longitude,
           city,
           state
    FROM ec_tmp.customer
)

INSERT
INTO ec_tmp.zip_code
SELECT zip_code_prefix::INTEGER      AS zip_code_id,

       zip_code_prefix               AS zip_code,
       substr(zip_code_prefix, 1, 1) AS zip_code_digit_1,
       substr(zip_code_prefix, 1, 2) AS zip_code_digit_2,
       substr(zip_code_prefix, 1, 3) AS zip_code_digit_3,
       substr(zip_code_prefix, 1, 4) AS zip_code_digit_4,
       min(latitude)                 AS latitude,
       min(longitude)                AS longitude,
       min(city)                     AS city,
       min(state)                    AS state
FROM zip_codes
GROUP BY zip_code_prefix;

SELECT util.add_index('ec_tmp', 'zip_code', column_names := ARRAY ['zip_code_id']);
