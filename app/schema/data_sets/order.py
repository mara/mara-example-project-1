from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.order import order_entity

order_data_set = DataSet(entity=order_entity,name='Orders')

order_data_set.include_attributes(['Customer', 'Zip code'], ['Zip code', 'City'])

order_data_set.add_simple_metric(
    name='# Order items',
    description='The number of order items in the order',
    aggregation=Aggregation.SUM,
    column_name='number_of_items')
order_data_set.add_simple_metric(
    name='Revenue',
    description='Revenue generated based on the price of the order',
    aggregation=Aggregation.SUM,
    column_name='revenue')
order_data_set.add_simple_metric(
    name='Total freight value',
    description='The freight value of the entire order (if an order has more than one item the freight value is split between items)',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
order_data_set.add_composed_metric(
    name='Avg. revenue per order item',
    description='The average revenue made in this order per order item',
    formula='[Revenue] / [# Order items]')
