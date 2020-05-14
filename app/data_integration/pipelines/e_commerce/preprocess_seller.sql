DROP TABLE IF EXISTS ec_tmp.seller CASCADE;

CREATE TABLE ec_tmp.seller
(
  seller_id       TEXT NOT NULL, -- seller unique identifier
  zip_code_prefix TEXT NOT NULL, -- integer representation of a zip_code_prefix
  city            TEXT,
  state           TEXT
);

INSERT INTO ec_tmp.seller
SELECT seller_id,
       zip_code_prefix,
       initcap(city) AS city,
       state
FROM ec_data.sellers;

SELECT util.add_index('ec_tmp', 'seller', column_names := ARRAY ['seller_id']);
