from mara_pipelines.commands.sql import ExecuteSQL


def create_cstore_table_for_query(sql_select_statement, database_schema, table_name, db_alias):
    """
    Create a cstore table for a that can take the output of a select statement.
    This function is needed because PostgreSQL does not have 'CREATE FOREIGN TABLE AS ... '
    """
    import mara_db.postgresql

    with mara_db.postgresql.postgres_cursor_context('dwh') as cursor:
        cursor.execute('SELECT oid, typname FROM pg_type;')
        db_types = {}
        for oid, type_name in cursor.fetchall():
            db_types[oid] = type_name

        cursor.execute(sql_select_statement + ' LIMIT 0')

        column_specs = []
        for column in cursor.description:
            column_specs.append(f'"{column.name}" {db_types[column.type_code]}')

        ddl = f"""
DROP FOREIGN TABLE IF EXISTS "{database_schema}"."{table_name}";
CREATE FOREIGN TABLE "{database_schema}"."{table_name}" (
"""
        ddl += ',\n    '.join(column_specs)
        ddl += "\n) SERVER cstore_server OPTIONS (compression 'pglz');"

        return ExecuteSQL(sql_statement=ddl, echo_queries=True, db_alias=db_alias).run()