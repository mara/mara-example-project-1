import pathlib

from data_integration.commands.sql import ExecuteSQL
from data_integration.pipelines import Pipeline, Task
from etl_tools.create_attributes_table import CreateAttributesTable
from mara_schema.config import data_sets, mondrian_schema
from mara_schema.schema import DataSet
from mara_schema.sql_generation import sql_for_flattened_table, sql_for_mondrian_fact_table

target_schema = mondrian_schema()['fact_table_schema_name']
tmp_schema = 'af_tmp'

pipeline = Pipeline(
    id="generate_artifacts",
    description="Generate flatten tables and mondrian fact table",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": f"{target_schema}"})

pipeline.add_initial(
    Task(
        id="initialize_schemas",
        description="Recreates the tmp and data schemas",
        commands=[
            ExecuteSQL(sql_statement=f"""
            DROP SCHEMA IF EXISTS {target_schema}_next CASCADE;
            CREATE SCHEMA {target_schema}_next;
            DROP SCHEMA IF EXISTS {tmp_schema} CASCADE;
            CREATE SCHEMA {tmp_schema};""", echo_queries=True)]))

for data_set in data_sets():
    task_id = f"create_{data_set.entity.name.replace(' ', '_').lower()}"

    pipeline.add(
        Task(id=f'{task_id}_flattened_table',
             description=f'Create {data_set.entity.name} flattened table',
             commands=[
                 ExecuteSQL(
                     sql_statement=lambda data_set=data_set: create_data_set_sql(data_set=data_set),
                     echo_queries=True)
             ]))
    pipeline.add(
        CreateAttributesTable(
            id=f"{task_id}_flattened_table_attributes",
            source_schema_name=f'{target_schema}_next',
            source_table_name=f'{data_set.entity.table_name}_flattened_table'),
        upstreams=[f'{task_id}_flattened_table'])

    pipeline.add(
        Task(id=f'{task_id}_mondrian_fact_table',
             description=f"Creates the {data_set.entity.name} mondrian fact table",
             commands=[ExecuteSQL(
                 sql_statement=lambda data_set=data_set: sql_for_mondrian_fact_table(data_set=data_set))]
             ))

pipeline.add_final(
    Task(
        id="replace_schema",
        description=f"Replaces the current {target_schema} schema with the contents of {target_schema}_next",
        commands=[
            ExecuteSQL(sql_statement=f"SELECT util.replace_schema('{target_schema}', '{target_schema}_next');")]))


def create_data_set_sql(data_set: DataSet, target_schema: str = target_schema, tmp_schema: str = tmp_schema):
    table_name = data_set.entity.table_name

    query = f"""DROP VIEW IF EXISTS {tmp_schema}.{table_name}_data_set_view CASCADE;
    
CREATE VIEW {tmp_schema}.{table_name}_data_set_view AS
{sql_for_flattened_table(data_set)};

DROP TABLE IF EXISTS {target_schema}_next."{table_name}_data_set" CASCADE;

CREATE TABLE {target_schema}_next."{table_name}_data_set" AS
SELECT *
FROM {tmp_schema}.{table_name}_data_set_view
LIMIT 0;

SELECT util.create_cstore_partition('{target_schema}_next', '{table_name}_data_set');
    
INSERT INTO {target_schema}_next."{table_name}_data_set_cstore"
SELECT *
FROM {tmp_schema}.{table_name}_data_set_view;
"""
    return query
