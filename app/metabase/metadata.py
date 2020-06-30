import sys
import time

import mara_schema.config
from mara_schema.metric import SimpleMetric, Aggregation

from app.metabase import config
from app.metabase.client import MetabaseClient


def update_metadata() -> bool:
    """Updates descriptions of tables & fields in Metabase, creates metrics and flushes field caches"""
    client = MetabaseClient()

    dwh_db_id = next(filter(lambda db: db['name'] == config.dwh_db_name(),
                            client.get('/api/database/')),
                     {}).get('id')

    if not dwh_db_id:
        print(f'Database {config.dwh_db_name()} not found in Metabase', file=sys.stderr)
        return False

    print('.. Triggering schema sync')
    client.post(f'/api/database/{dwh_db_id}/sync_schema')

    seconds = config.seconds_to_wait_for_schema_sync()
    print(f'.. Waiting {seconds} seconds')
    time.sleep(seconds)

    metadata = client.get(f'/api/database/{dwh_db_id}/metadata')
    data_sets = {data_set.name: data_set for data_set in mara_schema.config.data_sets()}

    for table in metadata['tables']:
        data_set = data_sets.get(table['name'])
        if data_set:
            client.put(f'/api/table/{table["id"]}',
                       {'description': data_set.entity.description,
                        'show_in_getting_started': True})
            _attributes = {}
            for path, attributes in data_set.connected_attributes().items():
                for name, attribute in attributes.items():
                    _attributes[name] = attribute
            for field in table['fields']:
                attribute = _attributes.get(field['name'], None)
                if attribute:
                    client.put(f'/api/field/{field["id"]}',
                               {'description': attribute.description or 'tbd',
                                'retired': 'normal', 'visibility_type': 'normal',
                                })
                else:
                    client.put(f'/api/field/{field["id"]}',
                               {'description': None, 'visibility_type': 'details-only'})

            for name, _metric in data_set.metrics.items():
                # https://github.com/metabase/metabase/blob/master/backend/mbql/src/metabase/mbql/schema.clj#L299
                if isinstance(_metric, SimpleMetric):
                    field = next(filter(lambda f: f['name'] == _metric.name, table['fields']), None)
                    if not field:
                        print(f'No field found for measure {_metric.name}', file=sys.stderr)
                    else:
                        metric = {'name': name, 'description': _metric.description, 'table_id': table['id'],
                                  'definition': {'source-table': table['id'],
                                                 'aggregation':
                                                     [[_metric.aggregation
                                                       if _metric.aggregation != Aggregation.DISTINCT_COUNT
                                                       else 'distinct',
                                                       ['field-id', field['id']]]]},
                                  'revision_message': 'Auto schema import'}
                        # elif isinstance(_metric, ComposedMetric):
                        #     customer_expressions = []
                        #     customer_expressions.append(_metric.formula_template.replace('{}', '').replace(' ', ''))
                        #     for parent_metric in _metric.parent_metrics:
                        #         field = next(filter(lambda f: f['name'] == parent_metric.name, table['fields']), None)
                        #         if not field:
                        #             print(f'No field found for measure {_metric.name}', file=sys.stderr)
                        #         else:
                        #             customer_expressions.append([parent_metric.aggregation, ['field-id', field['id']]])
                        #     metric = {'name': name, 'description': _metric.description, 'table_id': table['id'],
                        #               'definition': {'source-table': table['id'],
                        #                              'aggregation': [['aggregation-options',
                        #                                               customer_expressions,
                        #                                               {'display-name':
                        #                                                   _metric.formula_template.format(
                        #                                                       *[metric.name for metric in
                        #                                                         _metric.parent_metrics])}]]},
                        #               'revision_message': 'Auto schema import'}

                        existing_metric = next(filter(lambda f: f['name'] == name, table['metrics']), None)
                        if existing_metric:
                            client.put(f'/api/metric/{existing_metric["id"]}', metric)
                        else:
                            client.post('/api/metric', metric)

            for metric in table['metrics']:
                if metric['name'] not in data_set.metrics:
                    client.put(f'/api/metric/{metric["id"]}',
                               {'archived': True, 'revision_message': 'Auto schema import'})

        else:
            client.put(f'/api/table/{table["id"]}',
                       {'visibility_type': 'hidden'})

    print('.. Discarding field values')
    client.post(f'/api/database/{dwh_db_id}/discard_values')

    print('.. Rescanning field values')
    client.post(f'/api/database/{dwh_db_id}/rescan_values')

    return True
