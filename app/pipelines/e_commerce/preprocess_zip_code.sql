DROP TABLE IF EXISTS ec_tmp.zip_code CASCADE;

CREATE TABLE ec_tmp.zip_code
(
    zip_code_id      INTEGER NOT NULL, -- Unique integer representation of the zip_code_prefix

    zip_code         TEXT    NOT NULL, -- First 5 digits of zip code
    city             TEXT    NOT NULL,
    state            TEXT    NOT NULL
);

WITH zip_codes AS (
    SELECT zip_code_prefix,
           initcap(city) AS city,
           state         AS state
    FROM ec_data.geolocation
    UNION ALL
    SELECT zip_code,
           city,
           state
    FROM ec_tmp.seller
    UNION ALL
    SELECT zip_code,
           city,
           state
    FROM ec_tmp.customer
)

INSERT
INTO ec_tmp.zip_code
SELECT zip_code_prefix::INTEGER      AS zip_code_id,

       zip_code_prefix               AS zip_code,
       min(city)                     AS city,
       min(state)                    AS state
FROM zip_codes
GROUP BY zip_code_prefix;

SELECT util.add_index('ec_tmp', 'zip_code', column_names := ARRAY ['zip_code_id']);
