import mara_data_explorer.config
import mara_data_explorer.data_set
from mara_app.monkey_patch import patch


@patch(mara_data_explorer.config.data_sets)
def _data_sets():
    from mara_schema.config import data_sets as mt_data_sets

    result = []

    for data_set in mt_data_sets():
        personal_data_column_names = []
        default_column_names = []
        for path, attributes in data_set.connected_attributes().items():
            for prefixed_name, attribute in attributes.items():
                if attribute.personal_data:
                    personal_data_column_names.append(prefixed_name)
                if attribute.important_field:
                    default_column_names.append(prefixed_name)

        for metric in data_set.metrics.values():
            if metric.important_field:
                default_column_names.append(metric.name)

        result.append(
            mara_data_explorer.data_set.DataSet(
                id=data_set.id(),
                name=data_set.name,
                database_alias='dwh',
                database_schema='data_sets',
                database_table=data_set.id(),
                personal_data_column_names=personal_data_column_names,
                default_column_names=default_column_names,
                use_attributes_table=True))
    return result


# adapt to the favorite chart color of your company
patch(mara_data_explorer.config.charts_color)(lambda: '#008000')
