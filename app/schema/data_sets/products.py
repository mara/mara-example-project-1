from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.product import product_entity

products_data_set = DataSet(entity=product_entity, name='Products')

products_data_set.add_simple_metric(
    name='# Order items',
    description='How many times this product has been sold (at the time of the last DWH import)',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
products_data_set.add_simple_metric(
    name='Revenue (all time)',
    description='The revenue generated from the product since the beginning it has been sold',
    aggregation=Aggregation.SUM,
    column_name='revenue_all_time')
products_data_set.add_simple_metric(
    name='Total shipping value',
    description='Total shipping value payed for this product since the beginning it has been sold',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
