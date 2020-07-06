from mara_schema.entity import Entity
from mara_schema.attribute import Type

deal_entity = Entity(
    name='Deal',
    description="Deals that were closed by a sales representative which makes marketing qualified leads becoming "
                "sellers with products published on marketplaces",
    schema_name='m_dim',
    table_name='deal')

deal_entity.add_attribute(
    name='Deal ID',
    description='The ID of the deal in the DWH',
    column_name='deal_id',
    type=Type.ID,
    high_cardinality=True)

deal_entity.add_attribute(
    name='Sales development representative ID',
    description='The ID of the Sales Development Representative as defined in the backend',
    column_name='sdr_id',
    type=Type.ID,
    high_cardinality=True)

deal_entity.add_attribute(
    name='Sales representative ID',
    description='The ID of the Sales Representative as defined in the backend',
    column_name='sr_id',
    type=Type.ID,
    high_cardinality=True)

deal_entity.add_attribute(
    name='Deal date',
    description='The date when the marketing qualified lead was closed and became a seller',
    column_name='deal_date',
    type=Type.DATE)

deal_entity.add_attribute(
    name='Business Segment',
    description='The business segment in which the seller provides products e.g., "household_utilities", '
                '"car_accessories". Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    column_name='business_segment',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Lead type',
    description='The type of the lead in terms of company size, type, and experience, e.g., "online_beginner",'
                ' "online_medium". Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    column_name='lead_type',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Lead behaviour profile',
    description='The behaviour profile of the lead based on the DISC behavior assessment tool '
                '(https://en.wikipedia.org/wiki/DISC_assessment). '
                'Identified by the Sales Development Representative on the first contact with the lead',
    column_name='lead_behaviour_profile',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Has company',
    description='Whether the lead has a company with formal documentation',
    column_name='has_company',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Has GTIN',
    description='Whether the lead has a Global Trade Item Number (barcode) for his products',
    column_name='has_gtin',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Average stock',
    description='The average number of items per product the lead has available on stock. '
                'Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    column_name='average_stock',
    type=Type.ENUM)

deal_entity.add_attribute(
    name='Business type',
    description='The type of business the lead has: reseller, manufacturer, other, or unknown',
    column_name='business_type',
    type=Type.ENUM)

from .marketing_qualified_lead import marketing_qualified_lead_entity
from .seller import seller_entity

deal_entity.link_entity(target_entity=marketing_qualified_lead_entity,
                        fk_column='marketing_qualified_lead_fk')
deal_entity.link_entity(target_entity=seller_entity, fk_column='seller_fk')
