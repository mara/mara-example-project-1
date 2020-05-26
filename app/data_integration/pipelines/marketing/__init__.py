import pathlib

from data_integration.commands.sql import ExecuteSQL
from data_integration.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="marketing",
    description="Builds the marketing-funnel cube based on Olist sellers' marketing funnel and e-commerce data",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "m_dim"})

pipeline.add_initial(
    Task(id="initialize_schemas",
         description="Recreates the schemas of the pipeline",
         commands=[
             ExecuteSQL(sql_file_name="recreate_schemas.sql")
         ]))

pipeline.add(
    Task(id="preprocess_marketing_qualified_lead",
         description="Pre-process the marketing qualified leads that are eligible to sell their products at Olist",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_marketing_qualified_lead.sql")
         ]))

pipeline.add(
    Task(id="preprocess_closed_deal",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_closed_deal.sql")
         ]))

pipeline.add(
    Task(id="transform_smaller_dimensions",
         description="Transform smaller marketing dimensions",
         commands=[
             ExecuteSQL(sql_file_name="transform_smaller_dimensions.sql")
         ]),
    upstreams=["preprocess_marketing_qualified_lead", "preprocess_closed_deal"])

pipeline.add(
    Task(id="transform_closed_deal",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_closed_deal.sql", echo_queries=False)
         ]),
    upstreams=["transform_smaller_dimensions"])

pipeline.add(
    Task(id="transform_marketing_qualified_lead",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_marketing_qualified_lead.sql", echo_queries=False)
         ]),
    upstreams=["transform_smaller_dimensions"])

pipeline.add(
    Task(id="transform_marketing_funnel",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_marketing_funnel.sql")
         ]),
    upstreams=["transform_marketing_qualified_lead", "transform_closed_deal"])

pipeline.add(
    Task(id="constrain_tables",
         description="Adds foreign key constrains between the dim tables",
         commands=[
             ExecuteSQL(sql_file_name="constrain_tables.sql", echo_queries=False)
         ]),
    upstreams=["transform_marketing_funnel"])

pipeline.add_final(
    Task(id="replace_schema",
         description="Replaces the current m_dim schema with the contents of m_dim_next",
         commands=[
             ExecuteSQL(sql_statement="SELECT util.replace_schema('m_dim', 'm_dim_next');")
         ]))
