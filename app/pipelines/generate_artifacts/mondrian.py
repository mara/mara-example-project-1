import pathlib

from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task
from etl_tools.create_attributes_table import CreateAttributesTable
from mara_schema.config import data_sets
from mara_schema.schema.data_set import DataSet
from mara_schema.artifact_generation.data_set_tables import sql_for_flattened_table, sql_for_star_schema_fact_table
from mara_pipelines.commands.python import RunFunction



pipeline = Pipeline(
    id="flatten_data_sets_for_mondrian",
    description="Creates data set tables for Mondrian (star schema, without composed metrics, without personal data)",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": 'mondrian'})

pipeline.add_initial(
    Task(
        id="initialize_schema",
        description="Recreates the mondrian schema",
        commands=[
            ExecuteSQL(sql_statement=f"""
DROP SCHEMA IF EXISTS mondrian_next CASCADE;
CREATE SCHEMA mondrian_next;
""", echo_queries=False)]))

for data_set in data_sets():
    pipeline.add(
        Task(id=f"flatten_{data_set.id()}_for_mondrian",
             description=f'Flattens the "{data_set.name}" data set for best use in Mondrian',
             commands=[
                 ExecuteSQL(f"""
CREATE TABLE mondrian_next."{data_set.entity.name}_star" AS
{sql_for_star_schema_fact_table(data_set)};
""")]))

