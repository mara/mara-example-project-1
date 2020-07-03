from mara_schema.entity import Entity
from mara_schema.attribute import Type

zip_code_entity = Entity(
    name='Zip code',
    description='Information on Brazilian zip codes including coordinates',
    schema_name='ec_dim',
    table_name='zip_code'
)

zip_code_entity.add_attribute(
    name='Geo-location ID',
    description='Unique identifier of a geo-location entry based on the zip code',
    column_name='zip_code_id',
    type=Type.ID,
    high_cardinality=True)
zip_code_entity.add_attribute(
    name='Zip code',
    description='First 5 digits of the zip code (Brazil has an 8-digit system)',
    important_field=True,
    column_name='zip_code')
zip_code_entity.add_attribute(
    name='Zip code 1st digit',
    description='First digit of the zip code',
    column_name='zip_code_digit_1')
zip_code_entity.add_attribute(
    name='Zip code 2nd digit',
    description='First 2 digits of the zip code',
    column_name='zip_code_digit_2')
zip_code_entity.add_attribute(
    name='Zip code 3rd digit',
    description='First 3 digits of the zip code',
    column_name='zip_code_digit_3')
zip_code_entity.add_attribute(
    name='Zip code 4th digit',
    description='First 4 digits of the zip code',
    column_name='zip_code_digit_4')
zip_code_entity.add_attribute(
    name='Latitude',
    description='Latitude coordinate',
    column_name='latitude',
    high_cardinality=True)
zip_code_entity.add_attribute(
    name='Longitude',
    description='Longitude coordinate',
    column_name='longitude',
    high_cardinality=True)
zip_code_entity.add_attribute(
    name='City',
    description='City name',
    column_name='city')
zip_code_entity.add_attribute(
    name='State',
    description='State name',
    column_name='state')
