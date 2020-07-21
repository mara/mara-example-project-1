import pathlib

from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="marketing",
    description="Builds the Leads cube based on marketing and e-commerce data",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "m_dim"})

pipeline.add_initial(
    Task(id="initialize_schemas",
         description="Recreates the schemas of the pipeline",
         commands=[
             ExecuteSQL(sql_file_name="recreate_schemas.sql")
         ]))

pipeline.add(
    Task(id="preprocess_lead",
         description="Preprocess the marketing leads",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_lead.sql")
         ]))

pipeline.add(
    Task(id="transform_smaller_dimensions",
         description="Transform smaller marketing dimensions",
         commands=[
             ExecuteSQL(sql_file_name="transform_smaller_dimensions.sql")
         ]),
    upstreams=["preprocess_lead"])

pipeline.add(
    Task(id="transform_lead",
         description="Creates the lead dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_lead.sql", echo_queries=False)
         ]),
    upstreams=["transform_smaller_dimensions"])

pipeline.add(
    Task(id="constrain_tables",
         description="Adds foreign key constrains between the dim tables",
         commands=[
             ExecuteSQL(sql_file_name="constrain_tables.sql", echo_queries=False)
         ]),
    upstreams=["transform_lead"])

pipeline.add_final(
    Task(id="replace_schema",
         description="Replaces the current m_dim schema with the contents of m_dim_next",
         commands=[
             ExecuteSQL(sql_statement="SELECT util.replace_schema('m_dim', 'm_dim_next');")
         ]))
