from mara_metadata.schema import Entity, Type

product_entity = Entity(
    name='Product',
    description='',
    schema_name='ec_dim')

product_entity.add_attribute(
    name='Product ID',
    description='',
    column_name='product_id',
    type=Type.ID,
    high_cardinality=True)
product_entity.add_attribute(
    name='Category',
    description='',
    column_name='category',
    type=Type.ID)
