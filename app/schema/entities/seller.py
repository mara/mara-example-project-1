from mara_schema.schema.entity import Entity
from mara_schema.schema.attribute import Type

seller_entity = Entity(
    name='Seller',
    description='Merchants that are selling their products through the Olist department store',
    schema_name='ec_dim')

from app.schema.entities.geo_location import geo_location_entity
from app.schema.entities.order import order_entity

seller_entity.link_entity(target_entity=order_entity, fk_column='first_order_fk',
                          prefix='First order')
seller_entity.link_entity(target_entity=order_entity, fk_column='last_order_fk',
                          prefix='Last order')
seller_entity.link_entity(target_entity=geo_location_entity, fk_column='geo_location_fk')

seller_entity.add_attribute(
    name='Seller ID',
    description='The unique identifier of the Seller',
    column_name='seller_id',
    type=Type.ID,
    high_cardinality=True)
