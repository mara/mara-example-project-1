import mara_metadata.config
from mara_app.monkey_patch import patch

from data_integration.config import default_db_alias
from mara_db.config import databases


@patch(mara_metadata.config.data_sets)
def _data_sets():
    from app.metadata.data_sets.order_item import order_item_data_set
    from app.metadata.data_sets.seller import seller_data_set
    from app.metadata.data_sets.customer import customer_data_set
    from app.metadata.data_sets.product import product_data_set
    from app.metadata.data_sets.marketing_funnel import marketing_funnel_data_set

    return [order_item_data_set, seller_data_set, customer_data_set, product_data_set, marketing_funnel_data_set]


patch(mara_metadata.config.schema_name)(lambda: 'Mara example project 1')
