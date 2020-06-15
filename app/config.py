"""Project specific configurations"""

import pathlib
import datetime
import mara_mondrian.config
from mara_app.monkey_patch import patch

patch(mara_mondrian.config.schema_file)(lambda: pathlib.Path('app/mondrian/schema.xml'))

def data_dir():
    """The directory where persistent input data is stored"""
    return pathlib.Path('./data')


def first_date():
    """The first date for which to process data (can be used to limit data volumes on local machine)"""
    return datetime.date(2017, 1, 1)