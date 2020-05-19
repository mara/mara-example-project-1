from mara_metadata.schema import Entity, Type

product_entity = Entity(
    name='Product',
    description='Products sold by Olist',
    schema_name='ec_dim')

product_entity.add_attribute(
    name='Product ID',
    description='Unique product identifier',
    column_name='product_id',
    type=Type.ID,
    high_cardinality=True)
product_entity.add_attribute(
    name='Category',
    description='Root category of product',
    column_name='category')
