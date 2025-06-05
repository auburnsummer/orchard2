from django_bridge.response import Response
from cafe.views.types import HttpRequest

from cafe.apps import RDLEVEL_INDEX_NAME
from orchard.settings import MEILI_API_URL, MEILI_API_KEY
import meilisearch

client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)

def search_levels(request: HttpRequest):
    # for now i'll just hardcode a query
    query = "jupiter"
    index = client.get_index(RDLEVEL_INDEX_NAME)
    results = index.search(query)
    print(results)
    return Response(request, request.resolver_match.view_name, {
        "message": "Search functionality coming soon!"
    }) 