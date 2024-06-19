from pathlib import Path
from django.apps import apps
from django.http import HttpResponse
from django.utils.cache import patch_cache_control
import re

from functools import cache

from orchard.settings import DEBUG

@cache
def _get_combined_css():
    style_regex = re.compile(r"<style data-hoist=\"true\">([\w\W]+?)<\/style>")

    cafe = apps.get_app_config("cafe")
    css_contents = []
    for jinja_file in (Path(cafe.path) / 'jinja2').glob('**/*.jinja'):
        with open(jinja_file) as f:
            contents = f.read()
            css_partial = "\n".join(style_regex.findall(contents))
            css_contents.append(css_partial)
    
    return "\n".join(css_contents)


def combined_css(_):
    css_content = _get_combined_css()

    response = HttpResponse(
        css_content,
        headers={
            'content-type': 'text/css'
        }
    )
    if DEBUG:
        patch_cache_control(response, no_cache=True)

    return response
