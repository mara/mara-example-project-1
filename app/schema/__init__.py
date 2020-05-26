import pathlib

import mara_schema.config
from mara_app.monkey_patch import patch


@patch(mara_schema.config.data_sets)
def _data_sets():
    from app.schema.data_sets.order_item import order_item_data_set
    from app.schema.data_sets.seller import seller_data_set
    from app.schema.data_sets.customer import customer_data_set
    from app.schema.data_sets.product import product_data_set
    from app.schema.data_sets.marketing_funnel import marketing_funnel_data_set

    return [order_item_data_set, seller_data_set, customer_data_set, product_data_set, marketing_funnel_data_set]


patch(mara_schema.config.mondrian_schema)(lambda: {
    "schema_name": "Mara example project 1",
    "fact_table_schema_name": "af_dim",
    "schema_file_dir": pathlib.Path('./app/mondrian')
})
