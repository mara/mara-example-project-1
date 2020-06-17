import pathlib

from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task
from etl_tools.create_attributes_table import CreateAttributesTable
from mara_schema.config import data_sets
from mara_schema.schema.data_set import DataSet
from mara_schema.artifact_generation.data_set_tables import sql_for_flattened_table, sql_for_star_schema_fact_table
from mara_pipelines.commands.python import RunFunction



from .cstore_tables import create_cstore_table_for_query

pipeline = Pipeline(
    id="flatten_data_sets_for_data_explorer",
    description="Creates data set tables for the Mara data explorer (completely flattened, with composed metrics & personal data)",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": 'data_sets'})


pipeline.add_initial(
    Task(
        id="initialize_schema",
        description="Recreates the data_sets schema",
        commands=[
            ExecuteSQL(sql_statement=f"""
DROP SCHEMA IF EXISTS data_sets_next CASCADE;
CREATE SCHEMA data_sets_next;
""", echo_queries=False)]))


for data_set in data_sets():
    def query(data_set):
        return sql_for_flattened_table(data_set)

    def create_cstore_table(data_set):
        return create_cstore_table_for_query(query(data_set), 'data_sets_next', data_set.id())

    task_id = f"flatten_{data_set.id()}_for_data_explorer"

    pipeline.add(
        Task(id=task_id,
             description=f'Flattens the "{data_set.name}" data set for best use in the Mara data explorer',
             commands=[
                 RunFunction(function=create_cstore_table, args=[data_set]),
                 ExecuteSQL(sql_statement=lambda data_set=data_set: f"""
INSERT INTO data_sets_next."{data_set.id()}"
{query(data_set)};
""")]))


    pipeline.add(
        CreateAttributesTable(
            id=f"create_attributes_table_for_{data_set.id()}",
            source_schema_name='data_sets_next',
            source_table_name=data_set.id()),
        upstreams=[task_id])

