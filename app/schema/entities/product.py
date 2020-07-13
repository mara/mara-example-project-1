from mara_schema.entity import Entity
from mara_schema.attribute import Type

product_entity = Entity(
    name='Product',
    description='Products that were at least sold once',
    schema_name='ec_dim')

product_entity.add_attribute(
    name='Product ID',
    description='The ID of the product as defined in the PIM system',
    column_name='product_id',
    type=Type.ID,
    high_cardinality=True)

product_entity.add_attribute(
    name='Product category',
    description='The category name describing the group of products (e.g. "health_beauty", '
                '"computers_accessories", etc.',
    column_name='product_category',
    important_field=True,
    type=Type.ENUM)

product_entity.add_attribute(
    name='Weight',
    description='The weight of the product measured in grams',
    column_name='weight')

product_entity.add_attribute(
    name='Length',
    description='The length of the product measured in centimeters',
    column_name='length')

product_entity.add_attribute(
    name='Height',
    description='The height of the product measured in centimeters',
    column_name='height')

product_entity.add_attribute(
    name='Width',
    description='The width of the product measured in centimeters',
    column_name='width')

product_entity.add_attribute(
    name='Number of photos',
    description='The number of published photos of this product on the store',
    column_name='number_of_photos')
