from mara_schema.schema.data_set import DataSet, Aggregation

from app.schema.entities.order_item import order_item_entity

order_item_data_set = DataSet(
    entity=order_item_entity,
    name='Order items',
    max_entity_link_depth=1)

order_item_data_set.include_path(['Order', 'Customer'])
order_item_data_set.include_path(['Order', 'Customer', 'Geo-location'])
order_item_data_set.include_attributes(['Order', 'Customer', 'Geo-location'], ['Zip code', 'City'])

order_item_data_set.include_path(['Seller', 'Geo-location'])
order_item_data_set.include_attributes(['Seller', 'Geo-location'], ['Zip code', 'City'])

order_item_data_set.include_path(['Order', 'Customer', ('Order','First order')])


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
