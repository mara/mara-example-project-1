from mara_schema.entity import Entity
from mara_schema.attribute import Type

customer_entity = Entity(
    name='Customer',
    description='People that made at least one order',
    schema_name='ec_dim')

customer_entity.add_attribute(
    name='Customer ID',
    description='The ID of the customer as defined in the backend',
    column_name='customer_id',
    type=Type.ID,
    high_cardinality=True)

customer_entity.add_attribute(
    name='Duration since first order',
    description='The number of days since the first order was placed',
    type=Type.DURATION,
    column_name='days_since_first_order',
    accessible_via_entity_link=False)

customer_entity.add_attribute(
    name='Duration since last order',
    description='The number of days since the last order was placed',
    type=Type.DURATION,
    column_name='days_since_last_order',
    accessible_via_entity_link=False)

customer_entity.add_attribute(
    name='Favourite product category',
    description='The category of the most purchased product (by revenue) of the customer',
    type=Type.ENUM,
    column_name='favourite_product_category',
    accessible_via_entity_link=False)

from .zip_code import zip_code_entity
from .order import order_entity

customer_entity.link_entity(
    target_entity=order_entity,
    fk_column='first_order_fk',
    prefix='First order')

customer_entity.link_entity(
    target_entity=order_entity,
    fk_column='last_order_fk',
    prefix='Last order')

customer_entity.link_entity(
    target_entity=zip_code_entity,
    prefix='',
    fk_column='zip_code_fk',
    description='The ZIP code info of the customer')
