from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.order_item import order_item_entity

order_item_data_set = DataSet(entity=order_item_entity, name='Order items')

order_item_data_set.add_simple_metric(
    name='# Orders',
    description='Number of distinct orders',
    aggregation=Aggregation.DISTINCT_COUNT,
    column_name='order_fk')
order_item_data_set.add_simple_metric(
    name='Revenue',
    description='Revenue generated based on the price of the item',
    aggregation=Aggregation.SUM,
    column_name='revenue')
order_item_data_set.add_simple_metric(
    name='Freight value',
    description='The freight value of the item (if an order has more than one item the freight value is split between items)',
    aggregation=Aggregation.SUM,
    column_name='freight_value')

order_item_data_set.exclude_path(['Seller', ('Order', 'First order')])
order_item_data_set.exclude_path(['Seller', ('Order', 'Last order')])

order_item_data_set.include_attributes(['Order', 'Customer', ('Order', 'First order')], ['Purchase date'])
order_item_data_set.include_attributes(['Order', 'Customer', ('Order', 'Last order')], ['Purchase date'])
order_item_data_set.include_attributes(['Order', 'Customer', 'Zip code'], ['Zip code', 'City'])

order_item_data_set.include_attributes(['Seller', 'Zip code'], ['Zip code', 'City'])
