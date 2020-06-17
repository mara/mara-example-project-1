from mara_schema.schema.data_set import DataSet, Aggregation

from app.schema.entities.customer import customer_entity

customer_data_set = DataSet(
    entity=customer_entity,
    name='Customers',
    max_entity_link_depth=1)

customer_data_set.add_simple_metric(
    name='Days since last order',
    description='Average number of days after the last order fulfillment by this seller',
    aggregation=Aggregation.AVERAGE,
    column_name='days_since_last_order')
customer_data_set.add_simple_metric(
    name='# Orders',
    description='Number of purchases made by this customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')
customer_data_set.add_simple_metric(
    name='# Order items',
    description='Number of items purchased by this customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
customer_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated of items purchased by this customer',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime')
customer_data_set.add_simple_metric(
    name='Total freight value',
    description='Total freight value of items purchased by this customer',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
customer_data_set.add_composed_metric(
    name='Avg. revenue per order',
    description='The average amount that the customer spent per order',
    formula='[Revenue (lifetime)] / [# Orders]')
