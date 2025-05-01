from django.templatetags.static import static
from django.urls import reverse
from jinja2 import ChoiceLoader, Environment, PackageLoader
from markupsafe import Markup, escape


def no_wrap(value):
    return Markup(f'<span class="nhsuk-u-nowrap">{escape(value)}</span>' if value else "")


def as_hint(value):
    return Markup(f'<span class="app-text-grey">{value}</span>' if value else "")


def format_words(value, separator="_"):
    """
    FIXME - ported from prototype
    * Format separated words as a sentence, preserving acronyms
    * Example: 'in_progress' becomes 'In progress'
    * Example: 'not_in_PACS' becomes 'Not in PACS'
    * Example: 'IBMs_server' becomes 'IBMs server'
    * Example: 'IBM's_mainframe' becomes 'IBM's mainframe'
    * @param {string} input - String to format
    * @param {string} [separator='_'] - Character that separates words
    * @returns {string} Formatted string as words
    """
    if not value:
        return ""

    parts = value.split(separator)
    result = []
    for part in parts:
        # Check for acronyms. Either:
        # - the whole thing is upper case
        # - there is an upper case character after the first letter
        if part == part.upper() or len(part) >= 2 and (part[1:].lower() != part[1:]):
            result.append(part)
        else:
            result.append(part.lower())

    return " ".join(parts)


def format_date(value):
    return value.strftime("%-d %B %Y")


def format_date_time(value):
    return value.strftime("%-d %B %Y, %H:%m")


def format_time(value):
    if value.minute == 0:
        if value.hour == 0:
            return "midnight"
        if value.hour == 12:
            return "midday"
        return value.strftime("%-I%p").lower()

    return value.strftime("%-I:%M%p").lower()


def format_time_range(value):
    start_time = format_time(value["start_time"])
    end_time = format_time(value["end_time"])
    return f"{start_time} to {end_time}"


def environment(**options):
    env = Environment(**options)
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
    env.filters["formatWords"] = format_words
    env.filters["formatDate"] = format_date
    env.filters["formatTimeString"] = format_date_time
    env.filters["formatRelativeDate"] = format_date
    env.filters["formatTimeRange"] = format_time_range
    return env
