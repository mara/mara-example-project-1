import pathlib

from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="e_commerce",
    description="Builds cubes related to the e-commerce public data by Olist",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "ec_dim"})

pipeline.add_initial(
    Task(id="initialize_schemas",
         description="Recreates the schemas of the pipeline",
         commands=[
             ExecuteSQL(sql_file_name="recreate_schemas.sql")
         ]))

pipeline.add(
    Task(id="preprocess_order",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_order.sql")
         ]))

pipeline.add(
    Task(id="preprocess_order_item",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_order_item.sql")
         ]),
    upstreams=["preprocess_order"])

pipeline.add(
    Task(id="preprocess_product",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_product.sql")
         ]))

pipeline.add(
    Task(id="preprocess_seller",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_seller.sql")
         ]))

pipeline.add(
    Task(id="preprocess_customer",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_customer.sql")
         ]))

pipeline.add(
    Task(id="preprocess_zip_code",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_zip_code.sql")
         ]),
    upstreams=["preprocess_seller", "preprocess_customer"])

pipeline.add(
    Task(id="transform_seller",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_seller.sql")
         ]),
    upstreams=["preprocess_zip_code", "preprocess_order_item"])

pipeline.add(
    Task(id="transform_order",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_order.sql")
         ]),
    upstreams=["preprocess_order_item"])

pipeline.add(
    Task(id="transform_customer",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_customer.sql")
         ]),
    upstreams=["preprocess_zip_code", "preprocess_order_item"])

pipeline.add(
    Task(id="transform_order_item",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_order_item.sql")
         ]),
    upstreams=["preprocess_order_item"])

pipeline.add(
    Task(id="transform_product",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_product.sql")
         ]),
    upstreams=["preprocess_product", "preprocess_order_item"])

pipeline.add(
    Task(id="transform_zip_code",
         description="",
         commands=[
             ExecuteSQL(sql_file_name="transform_zip_code.sql")
         ]),
    upstreams=["preprocess_zip_code"])

pipeline.add(
    Task(id="constrain_tables",
         description="Adds foreign key constrains between the dim tables",
         commands=[
             ExecuteSQL(sql_file_name="constrain_tables.sql", echo_queries=False)
         ]),
    upstreams=["transform_seller",
               "transform_customer",
               "transform_order_item",
               "transform_order",
               "transform_zip_code"])

pipeline.add_final(
    Task(id="replace_schema",
         description="Replaces the current ec_dim schema with the contents of ec_dim_next",
         commands=[
             ExecuteSQL(sql_statement="SELECT util.replace_schema('ec_dim', 'ec_dim_next');")
         ]))
