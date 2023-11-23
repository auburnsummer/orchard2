import logging

from orchard.libs.vitals.utils import dig
from orchard.libs.vitals.color_tagged_string import parse_color_tagged_string

logger = logging.getLogger(__name__)


def make_key_facet(path, fallback=None):
    def inner(obj, **kwargs):
        try:
            return dig(path, obj)
        except KeyError:
            logger.info(f"Key {path} not found, going to fallback.")
            return fallback

    return inner


def make_color_enabled_key_facet(path, fallback=None):
    def inner(obj, **kwargs):
        try:
            content = dig(path, obj)
            stripped, _ = parse_color_tagged_string(content)
            return stripped
        except KeyError:
            logger.info(f"Key {path} not found, going to fallback.")
            return fallback

    return inner