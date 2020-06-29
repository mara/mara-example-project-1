"""Metabase API integration"""


def external_metabase_url():
    """The URL under which the Metabase instance can be reached by users e.g. https://metabase.bi.example.com"""
    return 'http://127.0.0.1:3000'


def internal_metabase_url():
    """The URL under which the Metabase instance can be reached by from mara (usually circumventing proxies etc.)"""
    return 'http://127.0.0.1:3000'


def metabase_admin_first_name() -> str:
    """The first name of the user for accessing the metabase api"""
    return 'root'


def metabase_admin_last_name() -> str:
    """The last name of the user for accessing the metabase api"""
    return '@localhost'


def metabase_admin_email() -> str:
    """The email of the user for accessing the metabase api"""
    return 'foo@bar.com'


def metabase_admin_password():
    """The password of the user for accessing the metabase api"""
    return '123abc'


def metabase_db_alias() -> str:
    """The db alias of the Metabase metadata database"""
    return 'metabase'


def dwh_db_alias() -> str:
    """The alias of the database that Metabase reads from"""
    return 'dwh'


def dwh_db_name() -> str:
    """The name (in Metabase) of the database that Metabase reads from"""
    return 'DWH'


def seconds_to_wait_for_schema_sync() -> int:
    """How many seconds to wait after an (asynchronous) schema sync has been triggered"""
    return 5
