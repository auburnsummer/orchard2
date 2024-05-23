from jinja2 import Environment, PackageLoader, select_autoescape

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse
        }
    )
    return env