import pathlib

from etl_tools import initialize_utils, create_time_dimensions
from mara_pipelines.pipelines import Pipeline, Task
from mara_pipelines.commands.sql import ExecuteSQL

pipeline = Pipeline(
    id="initialize_db",
    description="Adds a number of utility functions & creates time dimensions",
    base_path=pathlib.Path(__file__).parent)

pipeline.add(initialize_utils.utils_pipeline(with_cstore_fdw=True))
pipeline.add(create_time_dimensions.pipeline, upstreams=['initialize_utils'])

pipeline.add(
    Task(id='create_read_only_user',
         description='Creates a read-only user "dwh_read_only", useful for giving analysts direct access to DWH',
         commands=[
             ExecuteSQL(sql_file_name='create_read_only_user.sql')
         ]),
    upstreams=['initialize_utils'])
