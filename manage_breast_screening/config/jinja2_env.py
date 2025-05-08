import re

from django.templatetags.static import static
from django.urls import reverse
from jinja2 import ChoiceLoader, Environment, PackageLoader
from markupsafe import Markup, escape

from ..utils.date_formatting import (
    format_date,
    format_date_time,
    format_relative_date,
    format_time,
    format_time_range,
)


def no_wrap(value):
    """
    Wrap a string in a span with class app-no-wrap

    >>> no_wrap('a really long string')
    Markup('<span class="nhsuk-u-nowrap">a really long string</span>')
    """
    return Markup(
        f'<span class="nhsuk-u-nowrap">{escape(value)}</span>' if value else ""
    )


def as_hint(value):
    """
    Wrap a string in a span with class app-text-grey

    >>> as_hint('Not provided')
    Markup('<span class="app-text-grey">Not provided</span>')
    """
    return Markup(f'<span class="app-text-grey">{value}</span>' if value else "")


def sentence_case(value):
    """
    Capitalise the first letter of a sentence.

    >>> sentence_case('a quick brown fox jumps over the lazy dog')
    'A quick brown fox jumps over the lazy dog'

    Unlike the built in `capitalize` filter, this will preserve
    capital letters already in the string:

    >>> sentence_case('not in PACS')
    'Not in PACS'
    """
    if not value:
        return ""

    return value[0].upper() + value[1:]


def format_nhs_number(value):
    """
    Format an NHS number with spaces

    >>> format_nhs_number('9998887777')
    '999 888 7777'
    """
    if not value:
        return ""

    digits = re.sub(r"\s", "", value)

    return f"{digits[:3]} {digits[3:6]} {digits[6:]}"


def environment(**options):
    env = Environment(**options, extensions=["jinja2.ext.do"])
    if env.loader:
        env.loader = ChoiceLoader([PackageLoader("nhsuk_frontend_jinja"), env.loader])

    env.globals.update(
        {
            "static": static,
            "url": reverse,
        }
    )
    env.filters["noWrap"] = no_wrap
    env.filters["asHint"] = as_hint
    env.filters["formatDate"] = format_date
    env.filters["formatDateTime"] = format_date_time
    env.filters["formatNhsNumber"] = format_nhs_number
    env.filters["formatRelativeDate"] = format_relative_date
    env.filters["formatTimeRange"] = format_time_range
    env.filters["formatTimeString"] = format_time
    env.filters["sentenceCase"] = sentence_case
    return env
