"""Project specific data integration settings"""

import datetime


def dev_limit() -> bool:
    """Whether or not to return less data (e.g. LIMIT 1000) when no time limit is available"""
    return ''


def number_of_chunks() -> int:
    return 7


def first_date() -> datetime.date:
    """Ignore data before this date"""
    return datetime.date(2016, 1, 1)
