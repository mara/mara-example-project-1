from mara_metadata.schema import DataSet, Aggregation

from app.metadata.entities.seller import seller_entity

seller_data_set = DataSet(
    entity=seller_entity,
    name='Sellers',
    max_entity_link_depth=1)

seller_data_set.add_simple_metric(
    name='# Sellers',
    description='The number of sellers',
    aggregation=Aggregation.COUNT,
    column_name='seller_id')
seller_data_set.add_simple_metric(
    name='Avg. days since last order',
    description='',
    aggregation=Aggregation.AVERAGE,
    column_name='days_since_last_order')
seller_data_set.add_simple_metric(
    name='# Orders',
    description='',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')
seller_data_set.add_simple_metric(
    name='# Order items',
    description='',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
seller_data_set.add_simple_metric(
    name='# Deliveries',
    description='',
    aggregation=Aggregation.SUM,
    column_name='number_of_deliveries')
seller_data_set.add_simple_metric(
    name='# Customers',
    description='',
    aggregation=Aggregation.SUM,
    column_name='number_of_customers')
seller_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime')
seller_data_set.add_simple_metric(
    name='Total freight value',
    description='',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
