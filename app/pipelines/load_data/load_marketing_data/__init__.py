import pathlib

from mara_pipelines.commands.sql import ExecuteSQL, Copy
from mara_pipelines.pipelines import Pipeline, Task
from mara_pipelines import config

pipeline = Pipeline(
    id="load_marketing_data",
    description="Jobs related with loading marketing leads data from the backend database",
    max_number_of_parallel_tasks=5,
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "m_data"})

pipeline.add_initial(
    Task(id="initialize_schemas", description="Recreates the marketing data schema",
         commands=[
             ExecuteSQL(sql_file_name='../recreate_marketing_data_schema.sql',
                        file_dependencies=[
                            pathlib.Path(__file__).parent.parent / 'recreate_marketing_data_schema.sql'])]))

tables = [
    'closed_deal',
    'marketing_qualified_lead'
]

for table in tables:
    pipeline.add(
        Task(id=f"load_{table}",
             description=f'Loads the {table}s from the backend database',
             commands=[

                 ExecuteSQL(sql_file_name=f'{table}/create_{table}_table.sql'),

                 Copy(sql_statement=f"""
                 SELECT *
                 FROM marketing.{table}s;
""",
                      source_db_alias='olist',
                      target_db_alias='dwh',
                      target_table=f'm_data.{table}',
                      delimiter_char=';')]
             )
    )
