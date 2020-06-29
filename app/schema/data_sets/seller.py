from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.seller import seller_entity

seller_data_set = DataSet(entity=seller_entity, name='Sellers')

seller_data_set.add_simple_metric(
    name='Avg. days since last order',
    description='Average number of days after the last order fulfillment by this seller',
    aggregation=Aggregation.AVERAGE,
    column_name='days_since_last_order')
seller_data_set.add_simple_metric(
    name='# Orders',
    description='Number of orders with at-least one item fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')
seller_data_set.add_simple_metric(
    name='# Order items',
    description='Number of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
seller_data_set.add_simple_metric(
    name='# Deliveries',
    description='Number of orders (with at-least one item fulfilled by this seller) that were already delivered to the customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_deliveries')
seller_data_set.add_simple_metric(
    name='# Customers',
    description='Number of customers with items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_customers')
seller_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime')
seller_data_set.add_simple_metric(
    name='Total freight value',
    description='Total freight value of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
seller_data_set.add_composed_metric(
    name='Avg. revenue per order',
    description='The average revenue that the seller made per order',
    formula='[Revenue (lifetime)] / [# Orders]')
