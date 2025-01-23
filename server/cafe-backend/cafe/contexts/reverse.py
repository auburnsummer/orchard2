from django.urls import URLPattern, URLResolver
from django.urls.resolvers import RegexPattern, RoutePattern
from cafe.views.types import HttpRequest
from typing import List

# some idea about passing the output of "reverse" as a context so that
# in the React side, we can use something akin to the Django url template tag.
# in Djangoland the typical idea is to define URLs only once in the urlconf, and
# everything else just refers to the urlconf: https://docs.djangoproject.com/en/5.1/topics/http/urls/#reverse-resolution-of-urls
# I think for now, to keep things simpler, we're not actually doing that for React yet.

def reverse(request: HttpRequest):
    # base path
    from cafe.urls import urlpatterns

    url_map = {}
    def get_urls(url_list: List[URLResolver | URLPattern]):
        for entry in url_list:
            if isinstance(entry, URLPattern):
                if entry.name:
                    pattern = entry.pattern
                    if isinstance(pattern, RegexPattern):
                        url_map[entry.name] = str(pattern.regex)
                    elif isinstance(pattern, RoutePattern): 
                        url_map[entry.name] = pattern._route
            if isinstance(entry, URLResolver):
                get_urls(entry.url_patterns)

    get_urls(urlpatterns)
    return url_map