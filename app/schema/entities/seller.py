from mara_schema.entity import Entity
from mara_schema.attribute import Type

seller_entity = Entity(
    name='Seller',
    description='Merchants that are selling their products through the Olist department store',
    schema_name='ec_dim')

from app.schema.entities.zip_code import zip_code_entity
from app.schema.entities.order import order_entity

seller_entity.link_entity(target_entity=order_entity, fk_column='first_order_fk',
                          prefix='First order')
seller_entity.link_entity(target_entity=order_entity, fk_column='last_order_fk',
                          prefix='Last order')
seller_entity.link_entity(target_entity=zip_code_entity, prefix='', fk_column='zip_code_fk')

seller_entity.add_attribute(
    name='Seller ID',
    description='The unique identifier of the Seller',
    column_name='seller_id',
    type=Type.ID,
    personal_data=True,
    high_cardinality=True)
