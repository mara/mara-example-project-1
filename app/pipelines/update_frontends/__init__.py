import pathlib

import mara_mondrian.config
import mara_mondrian.connection
import mara_schema.config
from mara_pipelines.commands.bash import RunBash
from mara_pipelines.commands.python import RunFunction
from mara_pipelines.pipelines import Pipeline, Task
from mara_pipelines.logging import logger

import mara_metabase.metadata

pipeline = Pipeline(
    id="update_frontends",
    description="Updates Metabase & Mondrian",
    base_path=pathlib.Path(__file__).parent)

pipeline.add(
    Task(id='update_metabase_metadata',
         description='Flushes all field value caches in Metabase and updates metadata',
         commands=[RunFunction(mara_metabase.metadata.update_metadata)]))

def write_mondrian_schema():
    import mara_mondrian.schema_generation
    file_name = pathlib.Path('.mondrian-schema.xml')
    logger.log(f'Writing {file_name}', logger.Format.ITALICS)

    mara_mondrian.schema_generation.write_mondrian_schema(
        file_name=pathlib.Path('.mondrian-schema.xml'),
        data_sets_table={data_set: ('mondrian', data_set.id()) for data_set in mara_schema.config.data_sets()},
        personal_data=False,
        high_cardinality_attributes=False)

    return True


pipeline.add(
    Task(id="update_mondrian_schema",
         description="Generates & reloads the mondrian schema & flushes all caches",
         commands=[
             RunFunction(write_mondrian_schema),
             RunBash(command=lambda: 'curl -s ' + mara_mondrian.config.mondrian_server_internal_url() + '/flush-caches')
         ]),
    upstreams=[])


