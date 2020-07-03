from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.order import order_entity

orders_data_set = DataSet(entity=order_entity,name='Orders')

orders_data_set.include_attributes(['Customer', 'Zip code'], ['Zip code', 'City'])

orders_data_set.add_simple_metric(
    name='# Order items',
    description='The number of ordered products',
    aggregation=Aggregation.SUM,
    column_name='number_of_items')
orders_data_set.add_simple_metric(
    name='Product revenue',
    description='The price of the ordered products as shown in the cart',
    aggregation=Aggregation.SUM,
    column_name='revenue')
orders_data_set.add_simple_metric(
    name='Shipping revenue',
    description='Revenue generated based on the price of the items and delivery fee (if an order has more than one item the freight value is split between items)',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
orders_data_set.add_composed_metric(
    name='Revenue',
    description='The total cart value of the order',
    formula='[Product revenue] + [Shipping revenue]',
    important_field=True)
orders_data_set.add_composed_metric(
    name='Avg. revenue per order item',
    description='The average revenue made in this order per order item',
    formula='[Revenue] / [# Order items]')
