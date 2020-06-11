import pathlib

from mara_pipelines.commands.sql import ExecuteSQL, Copy
from mara_pipelines.pipelines import Pipeline, Task
from mara_pipelines import config

pipeline = Pipeline(
    id="load_marketing_data",
    description="Jobs related with loading marketing data from the Olist back-end database",
    max_number_of_parallel_tasks=5,
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "m_data"})

pipeline.add_initial(
    Task(id="initialize_schemas", description="Recreates the marketing data schema",
         commands=[
             ExecuteSQL(sql_file_name='../recreate_marketing_data_schema.sql',
                        file_dependencies=[pathlib.Path(__file__).parent.parent / 'recreate_marketing_data_schema.sql'])]))

pipeline.add(
    Task(
        id="load_closed_deal_data",
        description="Loads the closed deals data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='closed_deal/create_closed_deal_table.sql'),
            Copy(sql_file_name='closed_deal/load_closed_deal_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='m_data.closed_deal',
                 delimiter_char=';',
                 replace={"@@first-date@@": lambda: config.first_date()})
        ]))

pipeline.add(
    Task(
        id="load_marketing_qualified_lead_data",
        description="Loads the marketing_qualified_leads data from the back-end DB",
        commands=[
            ExecuteSQL(sql_file_name='marketing_qualified_lead/create_marketing_qualified_lead_table.sql'),
            Copy(sql_file_name='marketing_qualified_lead/load_marketing_qualified_lead_data.sql', source_db_alias='olist',
                 target_db_alias='dwh', target_table='m_data.marketing_qualified_lead',
                 delimiter_char=';',
                 replace={"@@first-date@@": lambda: config.first_date()})
        ]))
