import pathlib

from mara_pipelines.commands.sql import ExecuteSQL, Copy
from mara_pipelines.pipelines import Pipeline, Task
from mara_pipelines import config

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
            ExecuteSQL(sql_file_name='customer/create_customer_table.sql'),
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
            ExecuteSQL(sql_file_name='geolocation/create_geolocation_table.sql'),
            Copy(sql_file_name='geolocation/load_geolocation_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.geolocation',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_order_item_data",
        description="Loads the order items data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order_item/create_order_item_table.sql'),
            Copy(sql_file_name='order_item/load_order_item_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order_item',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_order_payment_data",
        description="Loads the order payments data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order_payment/create_order_payment_table.sql'),
            Copy(sql_file_name='order_payment/load_order_payment_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order_payment',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_order_review_data",
        description="Loads the order reviews data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order_review/create_order_review_table.sql'),
            Copy(sql_file_name='order_review/load_order_review_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order_review',
                 delimiter_char=';',
                 replace={"@@first-date@@": lambda: config.first_date()})
        ]))

pipeline.add(
    Task(
        id="load_order_data",
        description="Loads the orders data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='order/create_order_table.sql'),
            Copy(sql_file_name='order/load_order_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.order',
                 delimiter_char=';',
                 replace={"@@first-date@@": lambda: config.first_date()})
        ]))

pipeline.add(
    Task(
        id="load_product_category_name_translation_data",
        description="Loads the product_category_name translation data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='product_category_name_translation/create_product_category_name_translation_table.sql'),
            Copy(sql_file_name='product_category_name_translation/load_product_category_name_translation_data.sql',
                 source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.product_category_name_translation',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_product_data",
        description="Loads the products data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='product/create_product_data_table.sql'),
            Copy(sql_file_name='product/load_product_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.product',
                 delimiter_char=';')
        ]))

pipeline.add(
    Task(
        id="load_seller_data",
        description="Loads the sellers data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='seller/create_seller_table.sql'),
            Copy(sql_file_name='seller/load_seller_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.seller',
                 delimiter_char=';')
        ]))
