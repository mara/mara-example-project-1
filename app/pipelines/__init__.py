"""Configures the data integration pipelines of the project"""

import datetime
import functools

import mara_pipelines.config
import etl_tools.config
from mara_pipelines.pipelines import Pipeline
from mara_app.monkey_patch import patch

import app.config

patch(mara_pipelines.config.data_dir)(lambda: app.config.data_dir())
patch(mara_pipelines.config.first_date)(lambda: app.config.first_date())
patch(mara_pipelines.config.default_db_alias)(lambda: 'dwh')


@patch(mara_pipelines.config.root_pipeline)
@functools.lru_cache(maxsize=None)
def root_pipeline():
    import app.pipelines.utils
    import app.pipelines.load_data.load_ecommerce_data
    import app.pipelines.load_data.load_marketing_data
    import app.pipelines.e_commerce
    import app.pipelines.marketing
    import app.pipelines.generate_artifacts
    import app.pipelines.consistency_checks
    import app.pipelines.update_frontends

    pipeline = Pipeline(
        id='mara_example_project_1',
        description='An example pipeline that integrates the Olist e-commerce and marketing funnel data')

    pipeline.add(app.pipelines.utils.pipeline)
    pipeline.add(app.pipelines.load_data.load_ecommerce_data.pipeline, upstreams=['utils'])
    pipeline.add(app.pipelines.load_data.load_marketing_data.pipeline, upstreams=['utils'])
    pipeline.add(app.pipelines.e_commerce.pipeline, upstreams=['load_ecommerce_data'])
    pipeline.add(app.pipelines.marketing.pipeline,
                 upstreams=['load_marketing_data', 'e_commerce'])
    pipeline.add(app.pipelines.generate_artifacts.pipeline, upstreams=['marketing'])
    pipeline.add(app.pipelines.update_frontends.pipeline, upstreams=['generate_artifacts'])
    pipeline.add(app.pipelines.consistency_checks.pipeline, upstreams=['update_frontends'])
    return pipeline


patch(etl_tools.config.number_of_chunks)(lambda: 11)
patch(etl_tools.config.first_date_in_time_dimensions)(lambda: app.config.first_date())
patch(etl_tools.config.last_date_in_time_dimensions)(
    lambda: datetime.datetime.utcnow().date() - datetime.timedelta(days=3))
