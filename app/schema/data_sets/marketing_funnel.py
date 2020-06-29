from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.marketing_funnel import marketing_funnel_entity

marketing_funnel_data_set = DataSet(entity=marketing_funnel_entity, name='Marketing funnel')

marketing_funnel_data_set.add_simple_metric(
    name='# Closed deals',
    description='The number of closed deals',
    aggregation=Aggregation.COUNT,
    column_name='closed_deal_fk')
marketing_funnel_data_set.add_simple_metric(
    name='# Orders',
    description='Number of orders with at-least one item fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')
marketing_funnel_data_set.add_simple_metric(
    name='# Order items',
    description='Number of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')
marketing_funnel_data_set.add_simple_metric(
    name='# Deliveries',
    description='Number of orders (with at-least one item fulfilled by this seller) that were already delivered to the customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_deliveries')
marketing_funnel_data_set.add_simple_metric(
    name='# Customers',
    description='Number of customers with items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_customers')
marketing_funnel_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime')
marketing_funnel_data_set.add_simple_metric(
    name='Total freight value',
    description='Total freight value of items fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='total_freight_value')
marketing_funnel_data_set.add_simple_metric(
    name='Declared product catalog size',
    description='Lead declared catalog size. Informed on contact',
    aggregation=Aggregation.SUM,
    column_name='declared_product_catalog_size')
marketing_funnel_data_set.add_simple_metric(
    name='Declared monthly revenue',
    description='Lead declared estimated monthly revenue. Informed on contact',
    aggregation=Aggregation.SUM,
    column_name='declared_monthly_revenue')
marketing_funnel_data_set.add_composed_metric(
    name='# Order per customer',
    description='Average number of orders per customer',
    formula='[# Orders] / [# Customers]')
