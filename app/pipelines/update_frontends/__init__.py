import pathlib

import mara_mondrian.config
import mara_mondrian.connection
# import mara_mondrian.mdx
# import mara_mondrian.schema
from mara_pipelines.commands.bash import RunBash
from mara_pipelines.logging import logger
from mara_pipelines.pipelines import Pipeline, Task, Command
from mara_pipelines.commands.sql import ExecuteSQL
from mara_pipelines.commands.python import RunFunction
from mara_page import html
import etl_tools.initialize_utils
from mara_data_explorer.config import data_sets
from app.pipelines.update_frontends.create_table_for_metabase import create_table_for_metabase
import mara_metabase.metadata

pipeline = Pipeline(
    id="update_frontends",
    description="Flushes the mondrian caches and updates Metabase",
    base_path=pathlib.Path(__file__).parent)

update_mondrian = Pipeline(
    id='update_mondrian',
    description='Reloads the mondrian schema, flushes all caches and warms them again',
    max_number_of_parallel_tasks=2,
    ignore_errors=True)

update_mondrian.add(
    Task(id="flush_mondrian_caches",
         description="Reloads the mondrian schema and flushes all caches",
         commands=[
             RunBash(command=lambda: 'curl -s ' + mara_mondrian.config.mondrian_server_internal_url() + '/flush-caches')
         ]),
    upstreams=[])



pipeline.add(update_mondrian)

update_frontend_db = Pipeline(
    id="update_frontend_db",
    description="Copies all tables that frontend should query to a separate db (for performance reasons)",
    max_number_of_parallel_tasks=3,
    base_path=pathlib.Path(__file__).parent)

utils_pipeline = etl_tools.initialize_utils.utils_pipeline(with_cstore_fdw=True)

update_frontend_db.add_initial(
    Task(id='initialize_frontend_db',
         description='Adds some functions to the frontend-db so that schema copying works',
         commands=[
             ExecuteSQL(sql_file_name='initialize_frontend_db.sql', db_alias='metabase'),
             ExecuteSQL(
                 sql_file_name=str(utils_pipeline.base_path() / 'schema_switching.sql'),
                 db_alias='metabase', echo_queries=False),
             ExecuteSQL(
                 sql_file_name=str(utils_pipeline.base_path() / 'cstore_fdw.sql'),
                 db_alias='metabase', echo_queries=False)
         ]))

for data_set in data_sets():
    task_id = f'copy_{data_set.name.lower().replace(" ", "_")}'
    update_frontend_db.add(
        Task(id=task_id, description=f'Copies the {data_set.name} to the metabase db',
             commands=[
                 RunFunction(function=create_table_for_metabase, args=[data_set.name,
                                                                       data_set.database_schema,
                                                                       data_set.database_table,
                                                                       'metabase_next'])
             ]))

update_frontend_db.add_final(
    Task(id='switch_metabase_schema',
         description='Replaces the current metabase schema in the metabase db with metabase_next',
         commands=[
             ExecuteSQL(sql_file_name='switch_metabase_schema.sql',
                        db_alias='metabase')
         ]))

pipeline.add(update_frontend_db)

pipeline.add(
    Task(id='update_metabase_metadata',
         description='Flushes all field value caches in Metabase and updates metadata',
         commands=[RunFunction(mara_metabase.metadata.update_metadata)]),
    upstreams=['update_frontend_db'])
