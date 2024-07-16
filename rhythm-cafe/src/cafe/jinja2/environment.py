from jinja2 import Environment, PackageLoader, select_autoescape

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

import datetime

from functools import partial
from compressor.contrib.jinja2ext import CompressorExtension
from django.contrib import messages
from orchard.settings import DEBUG

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "now": partial(datetime.datetime.now, datetime.UTC),
            "get_messages": messages.get_messages
        }
    )
    if DEBUG:
        env.cache = None
    env.add_extension(CompressorExtension)
    return env