from mara_metadata.schema import Entity, Type

seller_entity = Entity(
    name='Seller',
    description='People that fulfilled orders made at Olist',
    schema_name='ec_dim')

from app.metadata.entities.geo_location import geo_location_entity
from app.metadata.entities.order import order_entity

seller_entity.link_entity(target_entity=order_entity, fk_column='first_order_fk',
                          prefix='First order')
seller_entity.link_entity(target_entity=order_entity, fk_column='last_order_fk',
                          prefix='Last order')
seller_entity.link_entity(target_entity=geo_location_entity, fk_column='geo_location_fk',
                          prefix='Geo-location')

seller_entity.add_attribute(
    name='Seller ID',
    description='The unique identifier of the Seller',
    column_name='seller_id',
    type=Type.ID,
    high_cardinality=True)
