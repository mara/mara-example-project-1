import flask

blueprint = flask.Blueprint('start_page', __name__)

from mara_page import bootstrap, _, response
import mara_data_explorer.config

@blueprint.route('/')
def start_page():
    return response.Response(
        title='Welcome',
        html=_.div(class_='row')[
            _.div(class_='col-lg-6')[
                bootstrap.card(
                    header_left=_.b['Data'],
                    body=[
                        _.p[
                            _.b[_.a(href='https://tableau.bi.traderepublic.com')[
                                _.span(class_='fa fa-bar-chart')[''], ' Tableau']],
                            ' &amp; ',
                            _.b[_.a(href=flask.url_for('mara_metabase.metabase'))[' Metabase']
                            ],
                            ': Company wide dashboards and analyses'],
                        _.p[
                            _.b[
                                _.a(href=flask.url_for('mara_data_explorer.index_page'))[
                                    _.span(class_='fa fa-table')[''], ' Explore']],
                            ': Raw data access & segmentation. Jump directly to ',

                            ', '.join([str(_.a(href=flask.url_for('mara_data_explorer.data_set_page',
                                                                  data_set_id=ds.id))[ds.name])
                                       for ds in mara_data_explorer.config.data_sets()])
                        ],
                        _.p[
                            _.b[
                                _.a(href=flask.url_for('mara_mondrian.saiku'))[
                                    _.span(class_='fa fa-bar-chart')[''], ' Saiku']],
                            ': Yet another ad hoc analysis tool']
                    ]
                )
            ],
            _.div(class_='col-lg-6')[
                bootstrap.card(
                    header_left=_.b['Documentation'],
                    body=[
                        _.p[
                            _.b[
                                _.a(href=flask.url_for('mara_schema.index_page'))[
                                    _.span(class_='fa fa-book')[''], ' Data sets']],
                            ': Documentation of attributes and metrics of all data sets'],
                        _.p[
                            _.b[
                                _.a(href=flask.url_for('mara_pipelines.node_page'))[
                                    _.span(class_='fa fa-wrench')[''], ' Pipelines']],
                            ': The data integration pipelines that create the DWH'],
                        _.p[
                            _.b[
                                _.a(href='/db/dwh')[
                                    _.span(class_='fa fa-database')[''], ' Database Schema']],
                            ': Schema of the DWH database']
                    ])
            ]])
