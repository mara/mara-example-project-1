import mara_db.postgresql
from mara_pipelines.commands.sql import ExecuteSQL, Copy


def create_table_for_metabase(metabase_table: str, source_schema: str,
                              source_table: str, target_schema: str):
    column_definitions = []

    with mara_db.postgresql.postgres_cursor_context('dwh') as cursor:
        cursor.execute(f'''
SELECT
  att.attname AS column_name,
  pg_catalog.format_type(att.atttypid, att.atttypmod) AS column_type
FROM pg_attribute att
  JOIN pg_class tbl ON tbl.oid = att.attrelid
  JOIN pg_namespace ns ON tbl.relnamespace = ns.oid
WHERE ns.nspname = {'%s'} AND tbl.relname = {'%s'} AND attnum > 0
ORDER BY attnum''', (source_schema, source_table))

        for column_name, column_type in cursor.fetchall():
            column_definitions.append(f'\n  "{column_name}" {column_type}')

    if not ExecuteSQL(sql_statement=f'''
CREATE FOREIGN TABLE {target_schema}."{metabase_table}" ({", ".join(column_definitions)})
SERVER cstore_server OPTIONS(compression 'pglz');
''',
                      echo_queries=False,
                      db_alias='metabase').run():
        return False

    if not Copy(sql_statement=f'COPY {source_schema}.{source_table}_cstore TO STDOUT NULL \'\'',
                source_db_alias='dwh',
                target_db_alias='metabase',
                target_table=f'{target_schema}.\\"{metabase_table}\\"').run():
        return False

    return True
