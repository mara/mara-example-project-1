from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.product import product_entity

products_data_set = DataSet(entity=product_entity, name='Products')

products_data_set.add_simple_metric(
    name='# Order items',
    description='How many times this product has been sold (at the time of the last DWH import)',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items',
    important_field=True)
products_data_set.add_simple_metric(
    name='Product revenue',
    description='The lifetime revenue generated from this product',
    aggregation=Aggregation.SUM,
    column_name='product_revenue')
products_data_set.add_simple_metric(
    name='Shipping revenue',
    description='The lifetime revenue generated from delivery fees for this product',
    aggregation=Aggregation.SUM,
    column_name='shipping_revenue')
products_data_set.add_composed_metric(
    name='Revenue',
    description='The total revenue generated from this product',
    formula='[Product revenue] + [Shipping revenue]',
    important_field=True)
