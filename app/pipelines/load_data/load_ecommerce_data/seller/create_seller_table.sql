--This table includes data about the sellers that fulfilled orders made at Olist.
--Use it to find the seller location and to identify which seller fulfilled each product.
DROP TABLE IF EXISTS ec_data.seller CASCADE;
CREATE TABLE ec_data.seller
(
    seller_id       TEXT, --seller unique identifier
    zip_code_prefix TEXT, --first 5 digits of seller zip code
    city            TEXT, --seller city name
    state           TEXT  --seller state
);
