from mara_metadata.schema import Entity, Type

order_entity = Entity(
    name='Order',
    description='',
    schema_name='ec_dim')

from app.metadata.entities.customer import customer_entity

order_entity.link_entity(target_entity=customer_entity, fk_column='customer_fk',
                         prefix='Customer')

order_entity.add_attribute(
    name='Order ID',
    description='',
    column_name='order_id',
    type=Type.ID,
    high_cardinality=True)
order_entity.add_attribute(
    name='Status',
    description='',
    column_name='status',
    type=Type.ID)
order_entity.add_attribute(
    name='Purchase date',
    description='',
    column_name='purchase_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Approved date',
    description='',
    column_name='approved_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Delivered carrier date',
    description='',
    column_name='delivered_carrier_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Delivered customer date',
    description='',
    column_name='delivered_customer_date',
    type=Type.DATE)
order_entity.add_attribute(
    name='Estimated delivery date',
    description='',
    column_name='estimated_delivery_date',
    type=Type.DATE)
