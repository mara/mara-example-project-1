from mara_schema.data_set import DataSet, Aggregation

from ..entities.customer import customer_entity

customers_data_set = DataSet(entity=customer_entity, name='Customers')

customers_data_set.exclude_path([('Order', 'First order'), 'Customer'])
customers_data_set.exclude_path([('Order', 'Last order'), 'Customer'])

customers_data_set.include_attributes(['Zip code'],
                                      ['Zip code', 'City', 'State'])
customers_data_set.include_attributes([('Order', 'First order')],
                                      ['Order date'])
customers_data_set.include_attributes([('Order', 'Last order')],
                                      ['Order date'])

customers_data_set.add_simple_metric(
    name='# Orders (lifetime)',
    description='Number of orders placed by this customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_orders_lifetime')

customers_data_set.add_simple_metric(
    name='Revenue (lifetime)',
    description='The lifetime revenue generated from products purchased by this customer',
    aggregation=Aggregation.SUM,
    column_name='revenue_lifetime',
    important_field=True)

customers_data_set.add_composed_metric(
    name='AOV',
    description='The average revenue per order of the customer',
    formula='[Revenue (lifetime)] / [# Orders (lifetime)]')
