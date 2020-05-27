from mara_schema.schema import Entity, Type

geo_location_entity = Entity(
    name='Geo-location',
    description='Information on Brazilian zip codes including coordinates',
    schema_name='ec_dim',
    table_name='geo_location'
)

geo_location_entity.add_attribute(
    name='Geo-location ID',
    description='Unique identifier of a geo-location entry based on the zip code',
    column_name='geo_location_id',
    type=Type.ID,
    high_cardinality=True)
geo_location_entity.add_attribute(
    name='Zip code',
    description='First 5 digits of the zip code',
    column_name='zip_code_prefix')
geo_location_entity.add_attribute(
    name='Zip code 1st digit',
    description='First digit of the zip code',
    column_name='zip_code_digit_1')
geo_location_entity.add_attribute(
    name='Zip code 2nd digit',
    description='First 2 digits of the zip code',
    column_name='zip_code_digit_2')
geo_location_entity.add_attribute(
    name='Zip code 3rd digit',
    description='First 3 digits of the zip code',
    column_name='zip_code_digit_3')
geo_location_entity.add_attribute(
    name='Zip code 4th digit',
    description='First 4 digits of the zip code',
    column_name='zip_code_digit_4')
geo_location_entity.add_attribute(
    name='Latitude',
    description='Latitude coordinate',
    column_name='latitude',
    high_cardinality=True)
geo_location_entity.add_attribute(
    name='Longitude',
    description='Longitude coordinate',
    column_name='longitude',
    high_cardinality=True)
geo_location_entity.add_attribute(
    name='City',
    description='City name',
    column_name='city')
geo_location_entity.add_attribute(
    name='State',
    description='State name',
    column_name='state')
