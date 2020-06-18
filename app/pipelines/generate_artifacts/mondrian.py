import pathlib

from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task
from mara_schema.sql_generation import data_set_sql_query, database_identifier
from mara_schema.config import data_sets

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
CREATE TABLE mondrian_next.{database_identifier(data_set.name)} AS
{data_set_sql_query(data_set=data_set, human_readable_columns=False, star_schema=True,
                    include_personal_data=False, include_high_cardinality_attributes=False)};
""",
                            echo_queries=False)]))
