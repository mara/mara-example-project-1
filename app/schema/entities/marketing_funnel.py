from mara_schema.schema.entity import Entity
from mara_schema.schema.attribute import Type

marketing_funnel_entity = Entity(
    name='Marketing funnel',
    description="Seller's customer journey based on Olist marketing funnel and e-commerce data",
    schema_name='m_dim',
    table_name='marketing_funnel')

from app.schema.entities.marketing_qualified_lead import marketing_qualified_lead_entity
from app.schema.entities.closed_deal import closed_deal_entity

marketing_funnel_entity.link_entity(target_entity=marketing_qualified_lead_entity,
                                    fk_column='marketing_qualified_lead_fk')
marketing_funnel_entity.link_entity(target_entity=closed_deal_entity,
                                    fk_column='closed_deal_fk')

marketing_funnel_entity.add_attribute(
    name='Is closed deal',
    description='If the qualified lead was turned into a closed deal',
    column_name='is_closed_deal',
    type=Type.ENUM)
