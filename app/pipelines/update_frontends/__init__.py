import pathlib

import mara_mondrian.config
import mara_mondrian.connection
import mara_mondrian.mdx
import mara_mondrian.schema
from mara_pipelines.commands.bash import RunBash
from mara_pipelines.logging import logger
from mara_pipelines.pipelines import Pipeline, Task, Command
from mara_page import html

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


class WarmMondrianCube(Command):
    def __init__(self, cube: mara_mondrian.schema.Cube) -> None:
        super().__init__()
        self.cube = cube

    def run(self) -> bool:
        for query in self.queries():
            logger.log(query, logger.Format.ITALICS)
            try:
                response = mara_mondrian.mdx.process_execute_response(mara_mondrian.connection.execute(query))
            except mara_mondrian.connection.MondrianError as e:
                logger.log(str(e), logger.Format.VERBATIM, is_error=True)
                return False

            logger.log(str(list(response['axes']['Axis0'].tuples[0].members.values())[0].name), logger.Format.VERBATIM)

        return True

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
        Task(id=cube_name.replace(' ', '_').lower(),
             description=f'Warms the dimension caches for the "{cube_name}" cube',
             commands=[WarmMondrianCube(cube)]),
        upstreams=['flush_mondrian_caches']
    )

pipeline.add(update_mondrian)
