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
    description='The category name describing the group of products (e.g. "health_beuty", "computers_accessories", etc.',
    column_name='product_category',
    important_field=True,
    type=Type.ENUM)
