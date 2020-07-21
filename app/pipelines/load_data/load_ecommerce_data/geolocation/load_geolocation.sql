SELECT geolocation_zip_code_prefix,
       geolocation_lat,
       geolocation_lng,
       regexp_replace(geolocation_city, ';', '.'), --replace ';' with '.' (';' used as delimiter)
       geolocation_state
FROM ecommerce.geolocation