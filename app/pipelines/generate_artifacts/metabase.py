import pathlib

from mara_pipelines.commands.python import RunFunction
from mara_pipelines.commands.sql import ExecuteSQL, Copy
from mara_pipelines.pipelines import Pipeline, Task
from mara_schema.config import data_sets
from mara_schema.sql_generation import data_set_sql_query

from .cstore_tables import create_cstore_table_for_query
from .. import initialize_db

pipeline = Pipeline(
    id="flatten_data_sets_for_metabase",
    description="Creates data set tables for Metabase (completely flattened, without composed metrics, without personal data)",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": 'metabase'})

pipeline.add_initial(
    Task(
        id="initialize_schema",
        description="Recreates the metabase schema",
        commands=[
            ExecuteSQL(sql_statement=f"""
DROP SCHEMA IF EXISTS util CASCADE;
CREATE SCHEMA util;            

DROP SCHEMA IF EXISTS metabase_next CASCADE;
CREATE SCHEMA metabase_next;
""", echo_queries=False, db_alias='metabase-data'),

            ExecuteSQL(sql_file_name=str(initialize_db.pipeline.base_path() / 'create_read_only_user.sql'),
                       db_alias='metabase-data'),

            ExecuteSQL(
                sql_file_name=str(
                    initialize_db.pipeline.nodes['initialize_utils'].base_path() / 'schema_switching.sql'),
                db_alias='metabase-data'),
            ExecuteSQL(
                sql_file_name=str(initialize_db.pipeline.nodes['initialize_utils'].base_path() / 'cstore_fdw.sql'),
                db_alias='metabase-data')
        ]))

for data_set in data_sets():
    def query(data_set):
        return data_set_sql_query(data_set=data_set, human_readable_columns=True, pre_computed_metrics=False,
                                  star_schema=False, personal_data=False,
                                  high_cardinality_attributes=True)


    def create_cstore_table(data_set):
        return create_cstore_table_for_query(query(data_set), 'metabase_next', data_set.name, 'metabase-data')


    pipeline.add(
        Task(id=f"flatten_{data_set.id()}_for_metabase",
             description=f'Flattens the "{data_set.name}" data set for best use in Metabase',
             commands=[
                 RunFunction(function=create_cstore_table, args=[data_set]),
                 Copy(sql_statement=lambda data_set=data_set: f"""
{query(data_set)};
""",
                      source_db_alias='dwh',
                      target_table=f'metabase_next."{data_set.name}"',
                      target_db_alias='metabase-data')]))
