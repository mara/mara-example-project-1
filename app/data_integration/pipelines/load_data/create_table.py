def get_column_definitions(data_table):

    column_definitions = []

    field_template = '\t{:<40}\t{:<40}\t{}'

    for col in data_table['data_table_fields']:
        if col['not_null']:
            column_definitions.append(field_template.format('"{}"'.format(col['name']), col['data_type'], 'NOT NULL'))
        else:
            column_definitions.append(field_template.format('"{}"'.format(col['name']), col['data_type'], 'NULL'))

    return column_definitions


def create_table_sql(target_schema_name, data_table):
    query = 'DROP TABLE IF EXISTS {}.{}; \n CREATE TABLE {}.{} (\n {}\n );\n'
    col_definitions = get_column_definitions(data_table)

    create_table_statement = query.format(target_schema_name, data_table['target_name'], target_schema_name,
                                          data_table['target_name'],
                                          ',\n'.join(col_definitions))

    return create_table_statement
