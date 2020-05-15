from mara_metadata.schema import Entity, Type

geo_location_entity = Entity(
    name='Geo-location',
    description='',
    schema_name='ec_dim',
    table_name='geo_location'
)

geo_location_entity.add_attribute(
    name='Geo-location ID',
    description='',
    column_name='geo_location_id',
    type=Type.ID,
    high_cardinality=True)
geo_location_entity.add_attribute(
    name='Zip code',
    description='',
    column_name='zip_code_prefix')
geo_location_entity.add_attribute(
    name='Latitude',
    description='',
    column_name='latitude',
    type=Type.ID,
    high_cardinality=True)
geo_location_entity.add_attribute(
    name='Longitude',
    description='',
    column_name='longitude',
    type=Type.ID,
    high_cardinality=True)
geo_location_entity.add_attribute(
    name='City',
    description='',
    column_name='city',
    type=Type.ID)
geo_location_entity.add_attribute(
    name='State',
    description='',
    column_name='state',
    type=Type.ID)
