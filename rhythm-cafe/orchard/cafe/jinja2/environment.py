from jinja2 import Environment, PackageLoader, select_autoescape

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

import datetime

from functools import partial


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "now": partial(datetime.datetime.now, datetime.UTC)
        }
    )
    return env