from mara_schema.entity import Entity

product_category_entity = Entity(
    name='Product category',
    description='A broad categorization of products as defined by the purchasing team',
    schema_name='ec_dim')

product_category_entity.add_attribute(
    name='Category name',
    description='The category name describing the group of products (e.g. "health_beuty" or "computers_accessories")',
    column_name='product_category')