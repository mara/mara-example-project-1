from mara_schema.entity import Entity
from mara_schema.attribute import Type

customer_entity = Entity(
    name='Customer',
    description='People that made a purchase at Olist store',
    schema_name='ec_dim')

from app.schema.entities.geo_location import geo_location_entity
from app.schema.entities.order import order_entity

customer_entity.link_entity(target_entity=order_entity, fk_column='first_order_fk',
                            prefix='First order')
customer_entity.link_entity(target_entity=order_entity, fk_column='last_order_fk',
                            prefix='Last order')
customer_entity.link_entity(target_entity=geo_location_entity, fk_column='geo_location_fk')

customer_entity.add_attribute(
    name='Customer ID',
    description='The unique identifier of the customer',
    column_name='customer_id',
    type=Type.ID,
    personal_data=True,
    high_cardinality=True)
