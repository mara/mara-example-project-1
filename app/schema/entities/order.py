from mara_schema.entity import Entity
from mara_schema.attribute import Type

order_entity = Entity(
    name='Order',
    description='Orders made at Olist Store at multiple marketplaces in Brazil',
    schema_name='ec_dim')

from app.schema.entities.customer import customer_entity

order_entity.link_entity(target_entity=customer_entity, fk_column='customer_fk', prefix='Customer')

order_entity.add_attribute(
    name='Order ID',
    description='Unique identifier of the order',
    column_name='order_id',
    type=Type.ID,
    high_cardinality=True)
order_entity.add_attribute(
    name='Order status',
    description='Reference to the order status (delivered, shipped, etc)',
    column_name='status',
    important_field=True,
    type=Type.ENUM)
order_entity.add_attribute(
    name='Purchase date',
    description='The Purchase timestamp',
    column_name='purchase_date',
    important_field=True,
    type=Type.DATE)
order_entity.add_attribute(
    name='Approved date',
    description='Payment approval timestamp',
    column_name='approved_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Delivered carrier date',
    description='Order posting timestamp (when was handled to the logistic partner)',
    column_name='delivered_carrier_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Delivered customer date',
    description='Actual order delivery date to the customer',
    column_name='delivered_customer_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Estimated delivery date',
    description='Estimated delivery date that was informed to customer at the purchase moment',
    column_name='estimated_delivery_date',
    type=Type.DATE)
