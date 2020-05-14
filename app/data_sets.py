import data_sets.config
import data_sets.data_set
from mara_app.monkey_patch import patch


@patch(data_sets.config.data_sets)
def _data_sets():
    return [
        # data_sets.data_set.DataSet(
        #     id='order-items', name='Order items',
        #     database_alias='dwh', database_schema='ec_dim', database_table='order_item_data_set',
        #     default_column_names=[],
        #     use_attributes_table=True),
    ]


# adapt to the favorite chart color of your company
patch(data_sets.config.charts_color)(lambda: '#008000')
