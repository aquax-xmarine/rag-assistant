from dateutil import parser
from datetime import date, time


def parse_date(date_str: str) -> date | None:
    try:
        return parser.parse(date_str).date()
    except Exception:
        return None


def parse_time(time_str: str) -> time | None:
    try:
        return parser.parse(time_str).time()
    except Exception:
        return None