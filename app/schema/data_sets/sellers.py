from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.seller import seller_entity

sellers_data_set = DataSet(entity=seller_entity, name='Sellers')

sellers_data_set.include_attributes(['Order'], ['Order date'])

sellers_data_set.add_simple_metric(
    name='# Orders',
    description='Number of orders with at-least one product fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders',
    important_field=True)

sellers_data_set.add_simple_metric(
    name='# Order items',
    description='Number of products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items',
    important_field=True)

sellers_data_set.add_simple_metric(
    name='# Deliveries',
    description='Number of orders that were already delivered to the customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_deliveries')

sellers_data_set.add_simple_metric(
    name='Product revenue',
    description='The lifetime revenue generated from products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='product_revenue')

sellers_data_set.add_simple_metric(
    name='Shipping revenue',
    description='The lifetime revenue generated from delivery fees by this seller',
    aggregation=Aggregation.SUM,
    column_name='shipping_revenue')

sellers_data_set.add_composed_metric(
    name='Revenue',
    description='The total revenue generated from this seller',
    formula='[Product revenue] + [Shipping revenue]',
    important_field=True)

sellers_data_set.add_composed_metric(
    name='AOV',
    description='The average revenue per order. Attention: not meaningful when split by product',
    formula='[Revenue] / [# Orders]')
