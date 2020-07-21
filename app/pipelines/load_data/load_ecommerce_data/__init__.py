import pathlib

from mara_pipelines.commands.sql import ExecuteSQL, Copy
from mara_pipelines.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="load_ecommerce_data",
    description="Jobs related with loading e-commerce data from the backend database",
    max_number_of_parallel_tasks=5,
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "ec_data"})

pipeline.add_initial(
    Task(id="initialize_schemas", description="Recreates the e-commerce data schema",
         commands=[
             ExecuteSQL(sql_file_name='../recreate_ecommerce_data_schema.sql',
                        file_dependencies=[
                            pathlib.Path(__file__).parent.parent / 'recreate_ecommerce_data_schema.sql'])]))

tables = [
    "customer",
    "order",
    "order_item",
    "product",
    "product_category_name_translation",
    "seller"
]

for table in tables:
    pipeline.add(
        Task(id=f"load_{table}",
             description=f'Loads the {table}s from the backend database',
             commands=[

                 ExecuteSQL(sql_file_name=f'{table}/create_{table}_table.sql'),

                 Copy(sql_statement=f"""
                 SELECT *
                 FROM ecommerce.{table}s;
""",
                      source_db_alias='olist',
                      target_db_alias='dwh',
                      target_table=f'ec_data.{table}',
                      delimiter_char=';')]
             )
    )

pipeline.add(
    Task(
        id="load_geolocation_data",
        description="Loads geolocation data from the backend DB, "
                    "containing information Brazilian zip codes and its lat/lng coordinates",
        commands=[
            ExecuteSQL(sql_file_name='geolocation/create_geolocation_table.sql'),
            Copy(sql_file_name='geolocation/load_geolocation.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='ec_data.geolocation',
                 delimiter_char=';')
        ]))
