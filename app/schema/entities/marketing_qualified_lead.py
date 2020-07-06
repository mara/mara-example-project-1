from mara_schema.entity import Entity
from mara_schema.attribute import Type

marketing_qualified_lead_entity = Entity(
    name='Marketing qualified lead',
    description="Leads that are qualified to sell their products at Olist, after selection based on a landing_page form",
    schema_name='m_dim',
    table_name='marketing_qualified_lead')

marketing_qualified_lead_entity.add_attribute(
    name='Marketing qualified lead ID',
    description='Marketing qualified lead unique identifier',
    column_name='marketing_qualified_lead_id',
    type=Type.ID,
    high_cardinality=True)

marketing_qualified_lead_entity.add_attribute(
    name='Is closed deal',
    description='If the qualified lead was turned into a closed deal',
    column_name='is_closed_deal',
    type=Type.ENUM)

marketing_qualified_lead_entity.add_attribute(
    name='First contact date',
    description='Date of the first contact solicitation',
    column_name='first_contact_date',
    type=Type.DATE)

marketing_qualified_lead_entity.add_attribute(
    name='Landing page ID',
    description='Landing page id where the lead was acquired',
    column_name='landing_page_id',
    type=Type.ENUM)

marketing_qualified_lead_entity.add_attribute(
    name='Origin',
    description='Type of media where the lead was acquired',
    column_name='origin',
    type=Type.ENUM)
