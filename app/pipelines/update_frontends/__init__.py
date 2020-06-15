import pathlib

import mara_mondrian.config
import mara_mondrian.connection
import mara_mondrian.mdx
import mara_mondrian.schema
from mara_pipelines.commands.bash import RunBash
from mara_pipelines.commands.python import RunFunction
from mara_pipelines.logging import logger
from mara_pipelines.pipelines import Pipeline, Task, ParallelTask
from mara_page import html
import mara_pipelines.config
import math
import more_itertools

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
             RunBash(command=lambda: 'curl -s ' + mara_mondrian.config.monsai_internal_url() + '/flush-caches')
         ]),
    upstreams=[])

def run_mdx_query(query) -> bool:

    logger.log(query, logger.Format.ITALICS)
    try:
        response = mara_mondrian.mdx.process_execute_response(mara_mondrian.connection.execute(query))
    except mara_mondrian.connection.MondrianError as e:
        logger.log(str(e), logger.Format.VERBATIM, is_error=True)
        return False

    logger.log(str(list(response['axes']['Axis0'].tuples[0].members.values())[0].name), logger.Format.VERBATIM)

    return True

class WarmMondrianCube(ParallelTask):
    def __init__(self, id: str, description: str, cube: mara_mondrian.schema.Cube, max_number_of_parallel_tasks: int = None) -> None:
        super().__init__(id,
                         description,
                         max_number_of_parallel_tasks=max_number_of_parallel_tasks)
        self.cube = cube

    def add_parallel_tasks(self, sub_pipeline: Pipeline) -> None:

        queries = self.queries()
        commands = []
        for query in queries:
            commands.append(RunFunction(run_mdx_query, args=[query]))

        chunk_size = math.ceil(len(commands) / (2 * mara_pipelines.config.max_number_of_parallel_tasks()))
        for n, chunk in enumerate(more_itertools.chunked(commands, chunk_size)):
            task = Task(id=str(n), description='Process a portion of the queries')
            task.add_commands(chunk)
            sub_pipeline.add(task)

    def queries(self):
        queries = []
        for dimension in self.cube.dimensions.values():
            for hierarchy in dimension.hierarchies.values():
                for level in hierarchy.levels:
                    if len(dimension.hierarchies) > 1:
                        queries.append(
                            f'SELECT [{dimension.name}.{hierarchy.name}].[{level}].Members.Item(0) ON COLUMNS FROM [{self.cube.name}]')
                    else:
                        queries.append(
                            f'SELECT [{dimension.name}].[{level}].Members.Item(0) ON COLUMNS FROM [{self.cube.name}]')

        return queries

    def html_doc_items(self) -> [(str, str)]:
        return [('Cube name', self.cube.name),
                ('MDX queries', html.highlight_syntax('\n'.join(self.queries()), 'tsql'))]

for cube_name, cube in mara_mondrian.schema.mondrian_schema().cubes.items():
    update_mondrian.add(
        WarmMondrianCube(
            id=cube_name.replace(' ', '_').lower(),
            description=f'Warms the dimension caches for the "{cube_name}" cube',
            cube=cube),
        upstreams=['flush_mondrian_caches'])

pipeline.add(update_mondrian)