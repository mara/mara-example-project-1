from mara_schema.entity import Entity
from mara_schema.attribute import Type

order_entity = Entity(
    name='Order',
    description='Valid orders for which an invoice was created',
    schema_name='ec_dim')

order_entity.add_attribute(
    name='Order ID',
    description='The ID of the order in the backend',
    column_name='order_id',
    type=Type.ID,
    high_cardinality=True)
order_entity.add_attribute(
    name='Order status',
    description='The current status of the order (delivered, shipped, etc)',
    column_name='status',
    important_field=True,
    accessible_via_entity_link=False,
    type=Type.ENUM)
order_entity.add_attribute(
    name='Order date',
    description='The date when the order was placed (stored in the backend)',
    column_name='purchase_date',
    important_field=True,
    type=Type.DATE)
order_entity.add_attribute(
    name='Approval date',
    description='The date when the customer\'s payment was approved',
    column_name='approved_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Shipping date',
    description='The date when the order was shipped, i.e., handed to the logistic partner',
    column_name='delivered_carrier_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Delivery date',
    description='The date when the order was delivered to the customer',
    column_name='delivered_customer_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Estimated delivery date',
    description='The estimated delivery date communicated to the customer at the time of order placement',
    column_name='estimated_delivery_date',
    type=Type.DATE)

from .customer import customer_entity

order_entity.link_entity(target_entity=customer_entity, fk_column='customer_fk', prefix='Customer')