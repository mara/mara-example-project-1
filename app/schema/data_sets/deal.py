from mara_schema.data_set import DataSet, Aggregation

from ..entities.deal import deal_entity

deals_data_set = DataSet(entity=deal_entity, name='Deals')

deals_data_set.add_simple_metric(
    name='Declared product catalog size',
    description='Lead declared catalog size. Informed on contact',
    aggregation=Aggregation.SUM,
    column_name='declared_product_catalog_size')
deals_data_set.add_simple_metric(
    name='Declared monthly revenue',
    description='Lead declared estimated monthly revenue. Informed on contact',
    aggregation=Aggregation.SUM,
    column_name='declared_monthly_revenue')
deals_data_set.add_simple_metric(
    name='# Orders',
    description='Number of orders with at-least one item fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')
deals_data_set.add_simple_metric(
    name='# Order items',
    description='Number of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
deals_data_set.add_simple_metric(
    name='# Deliveries',
    description='Number of orders (with at-least one item fulfilled by this seller) that were already delivered to the customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_deliveries')
deals_data_set.add_simple_metric(
    name='# Customers',
    description='Number of customers with items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_customers')
deals_data_set.add_simple_metric(
    name='CLV',
    description='The lifetime revenue generated of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime')
deals_data_set.add_simple_metric(
    name='Total shipping value',
    description='Total shipping value of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='total_shipping_value')
