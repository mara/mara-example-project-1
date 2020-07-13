from mara_schema.data_set import DataSet, Aggregation

from ..entities.product import product_entity

products_data_set = DataSet(entity=product_entity, name='Products')

products_data_set.add_simple_metric(
    name='# Order items (lifetime)',
    description='How many times this product has been sold (at the time of the last DWH import)',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items',
    important_field=True)

products_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated from this product',
    aggregation=Aggregation.SUM,
    column_name='product_revenue')
