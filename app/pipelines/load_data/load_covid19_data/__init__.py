import pathlib

from mara_pipelines.commands.sql import ExecuteSQL, Copy
from mara_pipelines.pipelines import Pipeline, Task
from mara_pipelines import config

pipeline = Pipeline(
    id="load_covid19_data",
    description="Jobs related with loading COVID 19 data from a singer tap",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "m_data"})

pipeline.add_initial(
    Task(id="initialize_schemas", description="Recreates the marketing data schema",
         commands=[
             ExecuteSQL(sql_file_name='../recreate_covid19_data_schema.sql',
                        file_dependencies=[
                            pathlib.Path(__file__).parent.parent / 'recreate_covid19_data_schema.sql'])]))

SELECTED_STREAMS = [

]
