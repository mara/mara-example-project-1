from mara_schema.entity import Entity
from mara_schema.attribute import Type

lead_entity = Entity(
    name='Lead',
    description="Leads that made contact through filling a request of contact on a landing page. Can become "
                "sellers if they close a deal with a Sales Representative",
    schema_name='m_dim',
    table_name='lead')

lead_entity.add_attribute(
    name='Lead ID',
    description='The ID of the lead as defined in the backend',
    column_name='lead_id',
    type=Type.ID,
    high_cardinality=True)

lead_entity.add_attribute(
    name='Is closed deal',
    description='Whether the qualified lead closed a deal with a Sales Representative and became a seller',
    column_name='is_closed_deal',
    type=Type.ENUM,
    important_field=True)

lead_entity.add_attribute(
    name='First contact date',
    description='The date the lead made first contact by signing up on a landing page',
    column_name='first_contact_date',
    important_field=True,
    type=Type.DATE)

lead_entity.add_attribute(
    name='Landing page ID',
    description='The ID of the landing page where the lead first made contact',
    column_name='landing_page_id',
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Advertising channel',
    description='Specific advertising channel the lead was acquired on',
    column_name='advertising_channel',
    important_field=True,
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Sales development representative ID',
    description='The ID of the Sales Development Representative as defined in the backend',
    column_name='sdr_id',
    type=Type.ID,
    high_cardinality=True)

lead_entity.add_attribute(
    name='Sales representative ID',
    description='The ID of the Sales Representative as defined in the backend',
    column_name='sr_id',
    type=Type.ID,
    high_cardinality=True)

lead_entity.add_attribute(
    name='Deal date',
    description='The date when the marketing qualified lead was closed and became a seller',
    column_name='deal_date',
    important_field=True,
    type=Type.DATE)

lead_entity.add_attribute(
    name='Business Segment',
    description='The business segment in which the seller provides products e.g., "household_utilities", '
                '"car_accessories". Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    column_name='business_segment',
    important_field=True,
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Lead type',
    description='The type of the lead in terms of company size, type, and experience, e.g., "online_beginner",'
                ' "online_medium". Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    column_name='lead_type',
    important_field=True,
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Lead behaviour profile',
    description='The behaviour profile of the lead based on the DISC behavior assessment tool '
                '(https://en.wikipedia.org/wiki/DISC_assessment). '
                'Identified by the Sales Development Representative on the first contact with the lead',
    column_name='lead_behaviour_profile',
    important_field=True,
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Has company',
    description='Whether the lead has a company with formal documentation',
    column_name='has_company',
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Has GTIN',
    description='Whether the lead has a Global Trade Item Number (barcode) for his products',
    column_name='has_gtin',
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Average stock',
    description='The average number of items per product the lead has available on stock. '
                'Provided by the lead on the sign up at a landing page or the first contact '
                'with a Sales Development Representative',
    column_name='average_stock',
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Business type',
    description='The type of business the lead has: reseller, manufacturer, other, or unknown',
    column_name='business_type',
    type=Type.ENUM)

lead_entity.add_attribute(
    name='Duration in days to closing the deal',
    description='The number of days it took from first contact with the lead '
                'to closing the deal by a Sales Representative and the lead becoming a seller',
    column_name='days_to_closing_deal',
    type=Type.DURATION
)

from .seller import seller_entity

lead_entity.link_entity(target_entity=seller_entity, fk_column='seller_fk')
