from mara_schema.data_set import DataSet, Aggregation

from ..entities.seller import seller_entity

sellers_data_set = DataSet(entity=seller_entity, name='Sellers')

sellers_data_set.exclude_path([('Order', 'First order'), 'Customer'])

sellers_data_set.include_attributes(['Zip code'],
                                    ['Zip code', 'City', 'State'])

sellers_data_set.include_attributes(['Order'], ['Order date'])

sellers_data_set.add_simple_metric(
    name='# Orders (lifetime)',
    description='Number of orders with at-least one product fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders_lifetime')

sellers_data_set.add_simple_metric(
    name='# Order items (lifetime)',
    description='Number of products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items_lifetime')

sellers_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated from products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime',
    important_field=True)

sellers_data_set.add_composed_metric(
    name='AOV',
    description='The average revenue per order. Attention: not meaningful when split by product',
    formula='[Revenue (lifetime)] / [# Orders (lifetime)]')
