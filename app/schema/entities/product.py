from mara_schema.entity import Entity
from mara_schema.attribute import Type

product_entity = Entity(
    name='Product',
    description='Products that were at least once sold',
    schema_name='ec_dim')

product_entity.add_attribute(
    name='Product ID',
    description='The ID of the product as defined in the PIM system',
    column_name='product_id',
    type=Type.ID,
    high_cardinality=True)

from .product_category import product_category_entity

product_entity.link_entity(target_entity=product_category_entity)
