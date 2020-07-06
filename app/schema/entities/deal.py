from mara_schema.entity import Entity
from mara_schema.attribute import Type

deal_entity = Entity(
    name='Deal',
    description="Marketing qualified leads that closed a deal with Olist and became sellers",
    schema_name='m_dim',
    table_name='deal')

deal_entity.add_attribute(
    name='Deal ID',
    description='Unique identifier of the deal in the DWH',
    column_name='deal_id',
    type=Type.ID,
    high_cardinality=True)

deal_entity.add_attribute(
    name='Sales development representative ID',
    description='Sales Development Representative unique identifier',
    column_name='sdr_id',
    type=Type.ID,
    high_cardinality=True)

deal_entity.add_attribute(
    name='Sales representative ID',
    description='Sales Representative unique identifier',
    column_name='sr_id',
    type=Type.ID,
    high_cardinality=True)

deal_entity.add_attribute(
    name='Won date',
    description='Date the deal was closed',
    column_name='won_date',
    type=Type.DATE)

deal_entity.add_attribute(
    name='Business Segment',
    description='Lead business segment. Informed on contact.',
    column_name='business_segment',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Lead type',
    description='Lead type. Informed on contact.',
    column_name='lead_type',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Lead behaviour profile',
    description='Lead behaviour profile. SDR identify it on contact',
    column_name='lead_behaviour_profile',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Has company',
    description='Does the lead have a company (formal documentation)?',
    column_name='has_company',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Has GTIN',
    description='Does the lead have Global Trade Item Number (barcode) for his products?',
    column_name='has_gtin',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Average stock',
    description='Lead declared average stock. Informed on contact',
    column_name='average_stock',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Business type',
    description='Type of business (reseller/manufacturer etc.)',
    column_name='business_type',
    type=Type.ENUM)

from .marketing_qualified_lead import marketing_qualified_lead_entity
from .seller import seller_entity

deal_entity.link_entity(target_entity=marketing_qualified_lead_entity,
                        fk_column='marketing_qualified_lead_fk')
deal_entity.link_entity(target_entity=seller_entity, fk_column='seller_fk')