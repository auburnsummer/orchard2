from django_bridge.response import Response

from cafe.management.commands.setupmeili import RDLEVEL_INDEX_NAME
from cafe.views.types import HttpRequest

from orchard.settings import MEILI_API_URL, MEILI_API_KEY
import meilisearch

client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)

def search_levels(request: HttpRequest):
    # for now i'll just hardcode a query
    query = "rdsrt"
    index = client.get_index(RDLEVEL_INDEX_NAME)
    results = index.search(query, {
        "attributesToSearchOn":  [
            "artist_tokens",
            "song",
            "song_alt",
            "description",
            "authors",
            "tags",
            "submitter.name",
            "club.name"
        ],
        "facets": [
            "artist_tokens",
            "difficulty",
            "single_player",
            "two_player",
            "tags",
            "has_classics",
            "has_oneshots",
            "has_squareshots",
            "has_freezeshots",
            "has_freetimes",
            "has_holds",
            "has_window_dance",
            "submitter.id",
            "club.id"
        ]
    })
    print(results)
    return Response(request, request.resolver_match.view_name, {
        "message": "Search functionality coming soon!"
    }) 