import pathlib

from mara_pipelines.commands.python import RunFunction
from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task
from mara_schema.sql_generation import data_set_sql_query
from mara_schema.config import data_sets

from .cstore_tables import create_cstore_table_for_query

pipeline = Pipeline(
    id="generate_artifacts",
    description="Generate data set tables suited for various front-ends",
    base_path=pathlib.Path(__file__).parent)

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
DROP SCHEMA IF EXISTS metabase_next CASCADE;
CREATE SCHEMA metabase_next;
""", echo_queries=False)]))

for data_set in data_sets():
    def query(data_set):
        return data_set_sql_query(data_set=data_set, human_readable_columns=True, pre_computed_metrics=False,
                                  star_schema=False, personal_data=False,
                                  high_cardinality_attributes=True)


    def create_cstore_table(data_set):
        return create_cstore_table_for_query(query(data_set), 'metabase_next', data_set.name)


    pipeline.add(
        Task(id=f"flatten_{data_set.id()}_for_metabase",
             description=f'Flattens the "{data_set.name}" data set for best use in Metabase',
             commands=[
                 RunFunction(function=create_cstore_table, args=[data_set]),
                 ExecuteSQL(sql_statement=lambda data_set=data_set: f"""
INSERT INTO metabase_next."{data_set.name}"
{query(data_set)};
""",
                            echo_queries=False)]))
