import pathlib

import mara_mondrian.config
import mara_mondrian.connection
from mara_pipelines.commands.bash import RunBash
from mara_pipelines.commands.python import RunFunction
from mara_pipelines.pipelines import Pipeline, Task

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

pipeline.add(
    Task(id='update_metabase_metadata',
         description='Flushes all field value caches in Metabase and updates metadata',
         commands=[RunFunction(mara_metabase.metadata.update_metadata)]))
