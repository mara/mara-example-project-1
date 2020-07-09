from mara_schema.data_set import DataSet, Aggregation

from ..entities.lead import lead_entity

leads_data_set = DataSet(entity=lead_entity, name='Leads')

leads_data_set.add_simple_metric(
    name='Declared product catalog size',
    description='The size of the product catalog that the lead has available to sell. '
                'Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    aggregation=Aggregation.SUM,
    column_name='declared_product_catalog_size')

leads_data_set.add_simple_metric(
    name='Declared monthly revenue',
    description='Estimated monthly revenue. '
                'Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    aggregation=Aggregation.SUM,
    column_name='declared_monthly_revenue')

leads_data_set.add_simple_metric(
    name='# Order items',
    description='Number of products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='number_of_order_items')

leads_data_set.add_simple_metric(
    name='# Deliveries',
    description='Number of orders fulfilled by this seller that were already delivered to the customer',
    aggregation=Aggregation.SUM,
    column_name='number_of_deliveries')

leads_data_set.add_simple_metric(
    name='Product revenue',
    description='The lifetime revenue generated from products sold by this seller',
    aggregation=Aggregation.SUM,
    column_name='product_revenue')

leads_data_set.add_simple_metric(
    name='Shipping revenue',
    description='The lifetime revenue generated from delivery fees by this seller',
    aggregation=Aggregation.SUM,
    column_name='shipping_revenue')

leads_data_set.add_composed_metric(
    name='Revenue',
    description='The total revenue generated from this seller',
    formula='[Product revenue] + [Shipping revenue]',
    important_field=True)
