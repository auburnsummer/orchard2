from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List

from django_bridge.response import Response

from cafe.management.commands.setupmeili import RDLEVEL_INDEX_NAME
from cafe.views.types import HttpRequest

from orchard.settings import MEILI_API_URL, MEILI_API_KEY
import meilisearch

client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)

RESULTS_PER_PAGE = 20

class ApprovalSearchOptions(Enum):
    ALL = auto()
    APPROVED_ONLY = auto()
    PENDING = auto()
    REJECTED_ONLY = auto()

@dataclass
class SearchLevelParams:
    q: str
    page: int
    approval: ApprovalSearchOptions
    min_bpm: Optional[float]
    max_bpm: Optional[float]
    difficulties: Optional[List[int]]
    single_player: Optional[bool]
    two_player: Optional[bool]

def get_search_params(request: HttpRequest):
    query = request.GET.get('q', "")
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    approval_options = ApprovalSearchOptions.APPROVED_ONLY
    if request.GET.get('peer_review') == "pending":
        approval_options = ApprovalSearchOptions.PENDING
    if request.GET.get('peer_review') == "rejected":
        approval_options = ApprovalSearchOptions.REJECTED_ONLY
    if request.GET.get("peer_review") == "all":
        approval_options = ApprovalSearchOptions.ALL

    min_bpm = request.GET.get('min_bpm', None)
    max_bpm = request.GET.get('max_bpm', None)

    difficulties_str = request.GET.getlist('difficulty', None)
    difficulties = None
    if difficulties_str:
        try:
            difficulties = [int(s) for s in difficulties_str]
        except ValueError:
            pass # it's none

    single_player_str = request.GET.get('single_player', None)
    single_player = None
    if single_player_str is not None:
        single_player = single_player_str == 'true'
    two_player_str = request.GET.get('two_player', None)
    two_player = None
    if two_player_str is not None:
        two_player = two_player_str == 'true'

    return SearchLevelParams(
        q=query,
        page=page,
        approval=approval_options,
        min_bpm=min_bpm,
        max_bpm=max_bpm,
        difficulties=difficulties,
        single_player=single_player,
        two_player=two_player,
    )


def search_levels(request: HttpRequest):
    params = get_search_params(request)
    offset = (params.page - 1) * RESULTS_PER_PAGE
    index = client.get_index(RDLEVEL_INDEX_NAME)
    filter = ""
    if params.approval == ApprovalSearchOptions.APPROVED_ONLY:
        filter += " AND approval >= 10"
    if params.approval == ApprovalSearchOptions.PENDING:
        filter += " AND approval = 0"
    if params.approval == ApprovalSearchOptions.REJECTED_ONLY:
        filter += " AND approval < 0"
    if params.min_bpm:
        filter += f" AND min_bpm >= {params.min_bpm}"
    if params.max_bpm:
        filter += f" AND max_bpm <= {params.max_bpm}"
    if params.difficulties:
        list_part = f"[{', '.join(str(i) for i in params.difficulties)}]"
        filter += f" AND difficulty IN {list_part}"
    if params.single_player is not None:
        filter += f" AND single_player = {params.single_player}"
    if params.two_player is not None:
        filter += f" AND two_player = {params.two_player}"
    results = index.search(params.q, {
        # we're only showing 20 results to the user
        # the 21st is to indicate if there is another page or not
        "limit": RESULTS_PER_PAGE + 1,
        "offset": offset,
        "filter": filter.lstrip(" AND "),
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
    return Response(request, request.resolver_match.view_name, {
        "results": results
    }) 