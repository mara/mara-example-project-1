from mara_schema.entity import Entity
from mara_schema.attribute import Type

marketing_qualified_lead_entity = Entity(
    name='Marketing qualified lead',
    description="Leads that made contact through filling a request of contact on a landing page",
    schema_name='m_dim',
    table_name='marketing_qualified_lead')

marketing_qualified_lead_entity.add_attribute(
    name='Marketing qualified lead ID',
    description='The ID of the marketing qualified lead as defined in the backend',
    column_name='marketing_qualified_lead_id',
    type=Type.ID,
    high_cardinality=True)

marketing_qualified_lead_entity.add_attribute(
    name='Is closed deal',
    description='Whether the qualified lead closed a deal with a Sales Representative and became a seller',
    column_name='is_closed_deal',
    type=Type.ENUM)

marketing_qualified_lead_entity.add_attribute(
    name='First contact date',
    description='The date the lead made first contact by signing up on a landing page',
    column_name='first_contact_date',
    important_field=True,
    type=Type.DATE)

marketing_qualified_lead_entity.add_attribute(
    name='Landing page ID',
    description='The ID of the landing page where the lead first made contact',
    column_name='landing_page_id',
    type=Type.ENUM)

marketing_qualified_lead_entity.add_attribute(
    name='Advertising channel',
    description='Specific advertising channel the lead was acquired on',
    column_name='advertising_channel',
    important_field=True,
    type=Type.ENUM)
