import pathlib

from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="e_commerce",
    description="Builds the e-commerce cubes and datasets",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "ec_dim"})

pipeline.add_initial(
    Task(id="initialize_schemas",
         description="Recreates the schemas of the pipeline",
         commands=[
             ExecuteSQL(sql_file_name="recreate_schemas.sql")
         ]))

pipeline.add(
    Task(id="preprocess_customer",
         description="Preprocess customers and consolidate the data to a single record per customer with "
                     "a unique ID",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_customer.sql")
         ]))

pipeline.add(
    Task(id="preprocess_order",
         description="Preprocess orders to get correct unique customer ID",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_order.sql")
         ]),
    upstreams=["preprocess_customer"])

pipeline.add(
    Task(id="preprocess_order_item",
         description="Preprocess order items to get correct unique customer ID",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_order_item.sql")
         ]),
    upstreams=["preprocess_order"])

pipeline.add(
    Task(id="preprocess_product",
         description="Preprocess products with product category in English",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_product.sql")
         ]))

pipeline.add(
    Task(id="preprocess_seller",
         description="Preprocess sellers and compute the seller's first order",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_seller.sql")
         ]))

pipeline.add(
    Task(id="preprocess_zip_code",
         description="Preprocess and collect zip codes from all data",
         commands=[
             ExecuteSQL(sql_file_name="preprocess_zip_code.sql")
         ]),
    upstreams=["preprocess_seller", "preprocess_customer"])

pipeline.add(
    Task(id="transform_zip_code",
         description="Creates the zip_code dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_zip_code.sql")
         ]),
    upstreams=["preprocess_zip_code"])

pipeline.add(
    Task(id="transform_seller",
         description="Creates the seller dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_seller.sql")
         ]),
    upstreams=["preprocess_order_item"])

pipeline.add(
    Task(id="transform_order",
         description="Creates the order dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_order.sql")
         ]),
    upstreams=["preprocess_order"])

pipeline.add(
    Task(id="transform_customer",
         description="Creates the customer dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_customer.sql")
         ]),
    upstreams=["preprocess_order_item", "preprocess_product"])

pipeline.add(
    Task(id="transform_order_item",
         description="Creates the order_item dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_order_item.sql")
         ]),
    upstreams=["preprocess_order_item"])

pipeline.add(
    Task(id="transform_product",
         description="Creates the product dim table",
         commands=[
             ExecuteSQL(sql_file_name="transform_product.sql")
         ]),
    upstreams=["preprocess_product", "preprocess_order_item"])

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
               "transform_product",
               "transform_zip_code"])

pipeline.add_final(
    Task(id="replace_schema",
         description="Replaces the current ec_dim schema with the contents of ec_dim_next",
         commands=[
             ExecuteSQL(sql_statement="SELECT util.replace_schema('ec_dim', 'ec_dim_next');")
         ]))
