from mara_schema.data_set import DataSet, Aggregation

from ..entities.product import product_entity

products_data_set = DataSet(entity=product_entity, name='Products')

products_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated from this product',
    aggregation=Aggregation.SUM,
    column_name='product_revenue',
    important_field=True)
