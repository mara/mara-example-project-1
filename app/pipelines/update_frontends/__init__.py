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
import app.metabase.metadata

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


# class WarmMondrianCube(Command):
#     def __init__(self, cube: mara_mondrian.schema.Cube) -> None:
#         super().__init__()
#         self.cube = cube
#
#     def run(self) -> bool:
#         for query in self.queries():
#             logger.log(query, logger.Format.ITALICS)
#             try:
#                 response = mara_mondrian.mdx.process_execute_response(mara_mondrian.connection.execute(query))
#             except mara_mondrian.connection.MondrianError as e:
#                 logger.log(str(e), logger.Format.VERBATIM, is_error=True)
#                 return False
#
#             logger.log(str(list(response['axes']['Axis0'].tuples[0].members.values())[0].name), logger.Format.VERBATIM)
#
#         return True
#
#     def queries(self):
#         queries = []
#         for dimension in self.cube.dimensions.values():
#             for hierarchy in dimension.hierarchies.values():
#                 for level in hierarchy.levels:
#                     if len(dimension.hierarchies) > 1:
#                         queries.append(
#                             f'SELECT [{dimension.name}.{hierarchy.name}].[{level}].Members.Item(0) ON COLUMNS FROM [{self.cube.name}]')
#                     else:
#                         queries.append(
#                             f'SELECT [{dimension.name}].[{level}].Members.Item(0) ON COLUMNS FROM [{self.cube.name}]')
#
#         return queries
#
#     def html_doc_items(self) -> [(str, str)]:
#         return [('Cube name', self.cube.name),
#                 ('MDX queries', html.highlight_syntax('\n'.join(self.queries()), 'tsql'))]


# for cube_name, cube in mara_mondrian.schema.mondrian_schema().cubes.items():
#     update_mondrian.add(
#         Task(id=cube_name.replace(' ', '_').lower(),
#              description=f'Warms the dimension caches for the "{cube_name}" cube',
#              commands=[WarmMondrianCube(cube)]),
#         upstreams=['flush_mondrian_caches']
#     )

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
         commands=[RunFunction(app.metabase.metadata.update_metadata)]),
    upstreams=['update_frontend_db'])
