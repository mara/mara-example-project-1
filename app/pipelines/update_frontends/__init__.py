import pathlib

import mara_mondrian.connection
import mara_schema.config
from mara_pipelines.commands.python import RunFunction
from mara_pipelines.logging import logger
from mara_pipelines.pipelines import Pipeline, Task

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
        data_set_tables={data_set: ('mondrian', data_set.id()) for data_set in mara_schema.config.data_sets()},
        personal_data=False,
        high_cardinality_attributes=False)

    return True


pipeline.add(
    Task(id="update_mondrian_server",
         description="Generates & reloads the mondrian schema & flushes all caches",
         commands=[
             RunFunction(write_mondrian_schema),
             RunFunction(mara_mondrian.connection.flush_mondrian_cache)
         ]),
    upstreams=[])
