from mara_metadata.schema import DataSet, Aggregation

from app.metadata.entities.order_item import order_item_entity

order_item_data_set = DataSet(
    entity=order_item_entity,
    name='Order items',
    max_entity_link_depth=1)

order_item_data_set.add_simple_metric(
    name='# Order items',
    description='The number of order items',
    aggregation=Aggregation.COUNT,
    column_name='order_item_id')
order_item_data_set.add_simple_metric(
    name='# Orders',
    description='',
    aggregation=Aggregation.DISTINCT_COUNT,
    column_name='order_fk')
order_item_data_set.add_simple_metric(
    name='Revenue',
    description='',
    aggregation=Aggregation.SUM,
    column_name='revenue')
order_item_data_set.add_simple_metric(
    name='Freight value',
    description='',
    aggregation=Aggregation.SUM,
    column_name='freight_value')
