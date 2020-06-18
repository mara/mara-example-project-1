from mara_schema.entity import Entity
from mara_schema.attribute import Type

order_item_entity = Entity(
    name='Order item',
    description='Items purchased within each order made at Olist Store',
    schema_name='ec_dim',
    table_name='order_item')

from app.schema.entities.order import order_entity
from app.schema.entities.product import product_entity
from app.schema.entities.seller import seller_entity

order_item_entity.link_entity(target_entity=order_entity, fk_column='order_fk')
order_item_entity.link_entity(target_entity=product_entity, fk_column='product_fk', prefix='Product')
order_item_entity.link_entity(target_entity=seller_entity, fk_column='seller_fk', prefix='Seller')

order_item_entity.add_attribute(
    name='Order item ID',
    description='Order item unique identifier',
    column_name='order_item_id',
    type=Type.ID,
    high_cardinality=True)
order_item_entity.add_attribute(
    name='Shipping limit date',
    description='The Seller shipping limit date for handling the order over to the logistic partner',
    column_name='shipping_limit_date',
    type=Type.DATE)
