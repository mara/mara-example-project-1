from mara_schema.data_set import DataSet, Aggregation

from ..entities.lead import lead_entity

leads_data_set = DataSet(entity=lead_entity, name='Leads')

leads_data_set.exclude_path(['Seller', ('Order', 'First order'), 'Customer'])

leads_data_set.include_attributes(['Seller', 'Zip code'],
                                  ['Zip code', 'City', 'State'])
leads_data_set.include_attributes(['Seller', ('Order', 'First order')],
                                  ['Order date'])

leads_data_set.add_simple_metric(
    name='# Orders (lifetime)',
    description='Number of orders with at-least one product fulfilled by this seller',
    aggregation=Aggregation.SUM,
    column_name='lifetime_number_of_orders')

leads_data_set.add_simple_metric(
    name='Lifetime sales',
    description='The lifetime revenue generated from products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='lifetime_sales',
    important_field=True)

leads_data_set.add_composed_metric(
    name='AOV',
    description='The average revenue per order. Attention: not meaningful when split by product',
    formula='[Lifetime sales] / [# Orders (lifetime)]')
