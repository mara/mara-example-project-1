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