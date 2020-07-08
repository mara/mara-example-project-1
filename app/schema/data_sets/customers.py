from mara_schema.data_set import DataSet, Aggregation

from app.schema.entities.customer import customer_entity

customers_data_set = DataSet(entity=customer_entity, name='Customers')

customers_data_set.add_simple_metric(
    name='# Orders',
    description='Number of orders placed by this customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders')

customers_data_set.add_simple_metric(
    name='# Order items',
    description='Number of items purchased by this customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')

customers_data_set.add_simple_metric(
    name='Product revenue',
    description='The lifetime revenue generated from items purchased by this customer',
    aggregation=Aggregation.SUM,
    column_name='product_revenue')

customers_data_set.add_simple_metric(
    name='Shipping revenue',
    description='The lifetime revenue generated from delivery fees payed by this customer',
    aggregation=Aggregation.SUM,
    column_name='shipping_revenue')

customers_data_set.add_composed_metric(
    name='CLV',
    description='The lifetime revenue generated from items purchased and delivery fees payed by this customer',
    formula='[Product revenue] + [Shipping revenue]')

customers_data_set.add_composed_metric(
    name='AOV',
    description='The average revenue per order of the customer',
    formula='[CLV] / [# Orders]')
