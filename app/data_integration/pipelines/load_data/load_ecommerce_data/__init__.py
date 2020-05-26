import pathlib

from data_integration.commands.sql import ExecuteSQL, Copy
from data_integration.pipelines import Pipeline, Task
from data_integration import config

pipeline = Pipeline(
    id="load_ecommerce_data",
    description="Jobs related with loading e-commerce data from the Olist back-end database",
    max_number_of_parallel_tasks=5,
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "ec_data"})

pipeline.add_initial(
    Task(id="initialize_schemas", description="Recreates the e-commerce data schema",
         commands=[
             ExecuteSQL(sql_file_name='../recreate_ecommerce_data_schema.sql',
                        file_dependencies=[pathlib.Path(__file__).parent.parent / 'recreate_ecommerce_data_schema.sql'])]))

pipeline.add(
    Task(
        id="load_customer_data",
        description="Loads the customers data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='customer/create_customer_data_table.sql'),
            Copy(sql_file_name='customer/load_customer_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.customer',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_geolocation_data",
        description="Loads geolocation data from the back-end DB, "
                    "containing information Brazilian zip codes and its lat/lng coordinates",
        commands=[
            ExecuteSQL(sql_file_name='geolocation/create_geolocation_data_table.sql'),
            Copy(sql_file_name='geolocation/load_geolocation_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.geolocation',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_order_item_data",
        description="Loads the order items data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order_item/create_order_item_data_table.sql'),
            Copy(sql_file_name='order_item/load_order_item_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order_item',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_order_payments_data",
        description="Loads the order payments data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order_payments/create_order_payments_data_table.sql'),
            Copy(sql_file_name='order_payments/load_order_payments_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order_payments',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_order_reviews_data",
        description="Loads the order reviews data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order_reviews/create_order_reviews_data_table.sql'),
            Copy(sql_file_name='order_reviews/load_order_reviews_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order_reviews',
                 delimiter_char=';',
                 replace={"@@first-date@@": lambda: config.first_date()})
        ]))

pipeline.add(
    Task(
        id="load_orders_data",
        description="Loads the orders data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='orders/create_orders_data_table.sql'),
            Copy(sql_file_name='orders/load_orders_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.orders',
                 delimiter_char=';',
                 replace={"@@first-date@@": lambda: config.first_date()})
        ]))

pipeline.add(
    Task(
        id="load_product_category_name_translation_data",
        description="Loads the product_category_name translation data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='product_category_name_translation/'
                                     'create_product_category_name_translation_data_table.sql'),
            Copy(sql_file_name='product_category_name_translation/load_product_category_name_translation_data.sql',
                 source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.product_category_name_translation',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_products_data",
        description="Loads the products data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='products/create_products_data_table.sql'),
            Copy(sql_file_name='products/load_products_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.products',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_sellers_data",
        description="Loads the sellers data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='sellers/create_sellers_data_table.sql'),
            Copy(sql_file_name='sellers/load_sellers_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.sellers',
                 delimiter_char=';')
        ]))
