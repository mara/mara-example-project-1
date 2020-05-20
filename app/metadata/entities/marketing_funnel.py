from mara_metadata.schema import Entity, Type

marketing_funnel_entity = Entity(
    name='Marketing funnel',
    description="Seller's customer journey based on Olist marketing funnel and e-commerce data",
    schema_name='m_dim',
    table_name='marketing_funnel')

from app.metadata.entities.seller import seller_entity

marketing_funnel_entity.link_entity(target_entity=seller_entity, fk_column='seller_fk', prefix='Seller')

marketing_funnel_entity.add_attribute(
    name='MQL ID',
    description='Marketing Qualified Lead unique identifier',
    column_name='mql_id',
    type=Type.ID,
    high_cardinality=True)

marketing_funnel_entity.add_attribute(
    name='Closed deal ID',
    description='Closed deal unique identifier referencing the MQL ID',
    column_name='closed_deal_id',
    type=Type.ID,
    high_cardinality=True)

marketing_funnel_entity.add_attribute(
    name='SDR id',
    description='Sales Development Representative unique identifier',
    column_name='sdr_id',
    type=Type.ID,
    high_cardinality=True)

marketing_funnel_entity.add_attribute(
    name='SR id',
    description='Sales Representative unique identifier',
    column_name='sr_id',
    type=Type.ID,
    high_cardinality=True)

marketing_funnel_entity.add_attribute(
    name='First contact date',
    description='Date of the first contact solicitation',
    column_name='first_contact_date',
    type=Type.DATE)

marketing_funnel_entity.add_attribute(
    name='Landing page ID',
    description='Landing page id where the lead was acquired',
    column_name='landing_page_id',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Origin',
    description='Type of media where the lead was acquired',
    column_name='origin',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Is closed deal',
    description='If the qualified lead was turned into a closed deals',
    column_name='is_closed_deal',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Won date',
    description='Date the deal was closed',
    column_name='won_date',
    type=Type.DATE)

marketing_funnel_entity.add_attribute(
    name='Business Segment',
    description='Lead business segment. Informed on contact.',
    column_name='business_segment',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Lead type',
    description='Lead type. Informed on contact.',
    column_name='lead_type',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Lead behaviour profile',
    description='Lead behaviour profile. SDR identify it on contact',
    column_name='lead_behaviour_profile',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Has company',
    description='Does the lead have a company (formal documentation)?',
    column_name='has_company',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Has GTIN',
    description='Does the lead have Global Trade Item Number (barcode) for his products?',
    column_name='has_gtin',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Average stock',
    description='Lead declared average stock. Informed on contact',
    column_name='average_stock',
    type=Type.ENUM)

marketing_funnel_entity.add_attribute(
    name='Business type',
    description='Type of business (reseller/manufacturer etc.)',
    column_name='business_type',
    type=Type.ENUM)
