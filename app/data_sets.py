import data_sets.config
import data_sets.data_set
from mara_app.monkey_patch import patch


@patch(data_sets.config.data_sets)
def _data_sets():
    from mara_schema.config import data_sets as mt_data_sets
    from mara_schema.schema import generate_attribute_name

    default_column_names = {
        'Orders': ['Order ID', 'Status', 'Purchase date', '# Order items',
                   'Revenue', 'Total freight value'],
        'Order items': ['Order item ID', 'Product category', 'Order status', 'Order purchase date',
                        'Order approved date', 'Order delivered customer date', 'Revenue', 'Freight value'],
        'Sellers': ['Seller ID', 'Last order purchase date', 'Geo-location city', '# Orders', '# Deliveries',
                    'Revenue (lifetime)'],
        'Customers': ['Customer ID', 'Geo-location city', 'Last order purchase date', '# Orders', 'Revenue (lifetime)'],
        'Products': ['Product ID', 'Category', '# Orders', '# Order items', '# Customers', 'Revenue (all time)',
                     'Total freight value'],
        'Marketing funnel': ['MQL ID', 'Closed deal ID', 'Seller ID', '# Orders', '# Order items', '# Customers',
                             'Revenue (all time)']
    }

    result = []

    for data_set in mt_data_sets():
        personal_data_column_names = []
        for path, attributes in data_set.connected_attributes().items():
            for attribute in attributes:
                if attribute.personal_data:
                    personal_data_column_names.append(generate_attribute_name(attribute, path))
        _data_set = data_sets.data_set.DataSet(
            id=data_set.name.replace(' ', '-').lower(), name=data_set.name,
            database_alias='dwh', database_schema='af_dim',
            database_table=f'{data_set.entity.table_name}_data_set',
            personal_data_column_names=personal_data_column_names,
            default_column_names=default_column_names[data_set.name],
            use_attributes_table=True
        )
        result.append(_data_set)

    return result


# adapt to the favorite chart color of your company
patch(data_sets.config.charts_color)(lambda: '#008000')
