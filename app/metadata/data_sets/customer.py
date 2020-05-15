from mara_metadata.schema import DataSet, Aggregation

from app.metadata.entities.customer import customer_entity

customer_data_set = DataSet(
    entity=customer_entity,
    name='Customers',
    max_entity_link_depth=1)

customer_data_set.add_simple_metric(
    name='# Customers',
    description='The number of customers',
    aggregation=Aggregation.COUNT,
    column_name='customer_id')
customer_data_set.add_simple_metric(
    name='Days since last order',
    description='',
    aggregation=Aggregation.AVERAGE,
    column_name='days_since_last_order')
customer_data_set.add_simple_metric(
    name='# Orders',
    description='',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')
customer_data_set.add_simple_metric(
    name='# Order items',
    description='',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
customer_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime')
customer_data_set.add_simple_metric(
    name='Total freight value',
    description='',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
