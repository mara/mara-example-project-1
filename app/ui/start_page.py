import flask

blueprint = flask.Blueprint('start_page', __name__)

from mara_page import bootstrap, _, response, html
import mara_data_explorer.config


@blueprint.route('/')
def start_page():
    import mara_pipelines.config

    from mara_data_explorer.data_set import find_data_set
    data_set_for_preview = find_data_set('order_items')
    assert (data_set_for_preview)

    return response.Response(
        title='MyCompany BI',
        html=_.div(class_='row')[
            _.div(class_='col-lg-6')[
                bootstrap.card(
                    header_left=_.b['Welcome'],
                    body=[
                        _.p['This is the first thing that users of your data warehouse will see. ',
                            'Please add links to relevant documentation, tutorials & other ',
                            'data tools in your organization.'
                        ],
                        _.p[_.a(href='https://github.com/mara/mara-example-project-1/blob/master/app/ui/start_page.py')[
                                'Here'],
                            ' is the source code for this page, and here is a picture of a ',
                            _.a(href='https://en.wikipedia.org/wiki/Mara_(mammal)')['mara'],
                            ':'
                        ],
                        _.img(src=flask.url_for('ui.static', filename='mara.jpg'),
                              style='width:40%; margin-left: auto; margin-right:auto; display:block;')

                    ]
                ),
                bootstrap.card(
                    header_left=[
                        _.b[_.a(href=flask.url_for('mara_metabase.metabase'))[
                            _.span(class_='fa fa-bar-chart')[''], ' Metabase']],
                        ' &amp; ',
                        _.b[_.a(href=flask.url_for('mara_mondrian.saiku'))[
                            _.span(class_='fa fa-bar-chart')[''], ' Saiku']],
                        ': Company wide dashboards, pivoting & ad hoc analysis'
                    ],
                    body=[
                        _.p['Metabase tutorial: ',
                            _.a(href='https://www.metabase.com/docs/latest/getting-started.html')[
                                'https://www.metabase.com/docs/latest/getting-started.html']],
                        _.p['Saiku introduction: ',
                            _.a(href='https://saiku-documentation.readthedocs.io/en/latest/')[
                                'https://saiku-documentation.readthedocs.io/en/latest/']]
                    ]
                ),
                bootstrap.card(
                    header_left=[
                        _.b[_.a(href=flask.url_for('mara_data_explorer.index_page'))[
                            _.span(class_='fa fa-table')[''], ' Explore']],
                        ': Raw data access & segmentation'
                    ],

                    body=[
                        _.p[
                            _.a(href=flask.url_for('mara_data_explorer.data_set_page',
                                                   data_set_id=data_set_for_preview.id))[
                                data_set_for_preview.name], ':',
                            html.asynchronous_content(flask.url_for('mara_data_explorer.data_set_preview',
                                                                    data_set_id=data_set_for_preview.id))
                        ],
                        _.p[
                            'Other data sets: ',
                            ', '.join([str(_.a(href=flask.url_for('mara_data_explorer.data_set_page',
                                                                  data_set_id=ds.id))[ds.name])
                                       for ds in mara_data_explorer.config.data_sets()
                                       if ds.id != data_set_for_preview.id])
                        ]
                    ]
                )
            ],
            _.div(class_='col-lg-6')[
                bootstrap.card(
                    header_left=[
                        _.b[_.a(href=flask.url_for('mara_schema.index_page'))[
                            _.span(class_='fa fa-book')[''], ' Data sets']],
                        ': Documentation of attributes and metrics of all data sets'
                    ],
                    body=html.asynchronous_content(url=flask.url_for('mara_schema.overview_graph'))
                ),
                bootstrap.card(
                    header_left=[
                        _.b[_.a(href=flask.url_for('mara_pipelines.node_page'))[
                            _.span(class_='fa fa-wrench')[''], ' Pipelines']],
                        ': The data integration pipelines that create the DWH'
                    ],
                    body=html.asynchronous_content(
                        flask.url_for('mara_pipelines.dependency_graph', path='/'))),
                bootstrap.card(
                    header_left=[
                        _.b[_.a(href=flask.url_for('mara_db.index_page'))[
                            _.span(class_='fa fa-database')[''], ' Database Schemas']],
                        ': Schemas of all databases connections'],
                    body=[
                        html.asynchronous_content(
                            flask.url_for('mara_db.draw_schema', db_alias=mara_pipelines.config.default_db_alias(),
                                          schemas='ec_dim'))
                    ]
                )
            ]
        ]
    )
