from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.order_item import order_item_entity

order_items_data_set = DataSet(entity=order_item_entity, name='Order items')

order_items_data_set.add_simple_metric(
    name='# Order items',
    description='The number of ordered products',
    column_name='order_item_id',
    aggregation=Aggregation.COUNT)
order_items_data_set.add_simple_metric(
    name='# Orders',
    description='The number of valid orders (orders with an invoice)',
    column_name='order_fk',
    aggregation=Aggregation.DISTINCT_COUNT,
    important_field=True)
order_items_data_set.add_simple_metric(
    name='Product revenue',
    description='The price of the ordered products as shown in the cart',
    aggregation=Aggregation.SUM,
    column_name='revenue',
    important_field=True)
order_items_data_set.add_simple_metric(
    name='Shipping revenue',
    description='Revenue generated based on the price of the items and delivery fee',
    aggregation=Aggregation.SUM,
    column_name='freight_value')
order_items_data_set.add_composed_metric(
    name='Revenue',
    description='The total cart value of the order',
    formula='[Product revenue] + [Shipping revenue]',
    important_field=True)
order_items_data_set.add_composed_metric(
    name='Avg. revenue per order item',
    description='The average revenue made in this order per order item',
    formula='[Revenue] / [# Order items]',
    important_field=True)

order_items_data_set.exclude_path(['Seller', ('Order', 'First order')])
order_items_data_set.exclude_path(['Seller', ('Order', 'Last order')])

order_items_data_set.include_attributes(['Order', 'Customer', ('Order', 'First order')], ['Order date'])
order_items_data_set.include_attributes(['Order', 'Customer', ('Order', 'Last order')], ['Order date'])
order_items_data_set.include_attributes(['Order', 'Customer', 'Zip code'], ['Zip code', 'City'])

order_items_data_set.include_attributes(['Seller', 'Zip code'], ['Zip code', 'City'])
