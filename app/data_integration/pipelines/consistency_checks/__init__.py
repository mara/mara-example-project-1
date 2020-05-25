import pathlib

from data_integration.commands.sql import ExecuteSQL
from data_integration.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="consistency_checks",
    description="Runs a set of queries to check the consistency of the transformed data",
    base_path=pathlib.Path(__file__).parent)

for file in pipeline.base_path().glob('**/*.sql'):
    relative_path = file.relative_to(pipeline.base_path())
    task_id = str(relative_path).replace('.sql', '').replace('/', '_').replace('-', '_')
    if task_id not in pipeline.nodes:
        pipeline.add(Task(
            id=task_id,
            description='Runs file ' + str(relative_path),
            commands=[ExecuteSQL(sql_file_name=str(relative_path), echo_queries=False)]))
