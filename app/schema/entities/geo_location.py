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
    description='First 5 digits of zip code',
    column_name='zip_code_prefix',
    type=Type.ENUM)
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
    column_name='city',
    type=Type.ENUM)
geo_location_entity.add_attribute(
    name='State',
    description='State name',
    column_name='state',
    type=Type.ENUM)
