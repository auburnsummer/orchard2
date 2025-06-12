from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List, Dict, Any, Union

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
    has_classics: Optional[bool]
    has_oneshots: Optional[bool]
    has_squareshots: Optional[bool]
    has_freezeshots: Optional[bool]
    has_freetimes: Optional[bool]
    has_holds: Optional[bool]
    has_window_dance: Optional[bool]
    tags_all: Optional[List[str]]
    tags_any: Optional[List[str]]
    authors_all: Optional[List[str]]
    artists_all: Optional[List[str]]
    seizure_warning: Optional[bool]

def parse_bool_param(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    return value.lower() == 'true'

def parse_int_param(value: Optional[str], min_value: Optional[int] = None) -> Optional[int]:
    if value is None:
        return None
    try:
        result = int(value)
        if min_value is not None and result < min_value:
            return min_value
        return result
    except ValueError:
        return None

def parse_float_param(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None

def get_search_params(request: HttpRequest) -> SearchLevelParams:
    """
    Parse and validate search parameters from the request.
    
    Args:
        request: The HTTP request containing search parameters
        
    Returns:
        SearchLevelParams: A dataclass containing the validated search parameters
    """
    # approval status
    approval_map: Dict[str, ApprovalSearchOptions] = {
        "pending": ApprovalSearchOptions.PENDING,
        "rejected": ApprovalSearchOptions.REJECTED_ONLY,
        "all": ApprovalSearchOptions.ALL
    }
    approval_str = request.GET.get('peer_review', '')
    approval = approval_map.get(approval_str, ApprovalSearchOptions.APPROVED_ONLY)
    
    # page
    page = parse_int_param(request.GET.get('page', '1'), min_value=1) or 1
    
    # bpm
    min_bpm = parse_float_param(request.GET.get('min_bpm'))
    max_bpm = parse_float_param(request.GET.get('max_bpm'))
    
    # difficulties
    difficulties_str = request.GET.getlist('difficulty')
    difficulties = None
    if difficulties_str:
        try:
            difficulties = [int(s) for s in difficulties_str]
        except ValueError:
            pass # then difficulties will stay as None
    
    # 1p/2p
    single_player = parse_bool_param(request.GET.get('single_player'))
    two_player = parse_bool_param(request.GET.get('two_player'))
    
    # step type filters
    has_classics = parse_bool_param(request.GET.get('has_classics'))
    has_oneshots = parse_bool_param(request.GET.get('has_oneshots'))
    has_squareshots = parse_bool_param(request.GET.get('has_squareshots'))
    has_freezeshots = parse_bool_param(request.GET.get('has_freezeshots'))
    has_freetimes = parse_bool_param(request.GET.get('has_freetimes'))
    has_holds = parse_bool_param(request.GET.get('has_holds'))
    has_window_dance = parse_bool_param(request.GET.get('has_window_dance'))

    # tags
    tags_all = request.GET.getlist('tags_all')
    tags_any = request.GET.getlist('tags_any')

    # authors
    authors_all = request.GET.getlist('authors_all')
    artists_all = request.GET.getlist('artists_all')

    seizure_warning = parse_bool_param(request.GET.get('seizure_warning'))

    
    return SearchLevelParams(
        q=request.GET.get('q', ""),
        page=page,
        approval=approval,
        min_bpm=min_bpm,
        max_bpm=max_bpm,
        difficulties=difficulties,
        single_player=single_player,
        two_player=two_player,
        has_classics=has_classics,
        has_oneshots=has_oneshots,
        has_squareshots=has_squareshots,
        has_freezeshots=has_freezeshots,
        has_freetimes=has_freetimes,
        has_holds=has_holds,
        has_window_dance=has_window_dance,
        tags_all=tags_all,
        tags_any=tags_any,
        authors_all=authors_all,
        artists_all=artists_all,
        seizure_warning=seizure_warning
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
    if params.has_classics is not None:
        filter += f" AND has_classics = {params.has_classics}"
    if params.has_oneshots is not None:
        filter += f" AND has_oneshots = {params.has_oneshots}"
    if params.has_squareshots is not None:
        filter += f" AND has_squareshots = {params.has_squareshots}"
    if params.has_freezeshots is not None:
        filter += f" AND has_freezeshots = {params.has_freezeshots}"
    if params.has_freetimes is not None:
        filter += f" AND has_freetimes = {params.has_freetimes}"
    if params.has_holds is not None:
        filter += f" AND has_holds = {params.has_holds}"
    if params.has_window_dance is not None:
        filter += f" AND has_window_dance = {params.has_window_dance}"
    if params.tags_all is not None:
        for tag in params.tags_all:
            filter += f" AND tags = {tag}"
    if params.tags_any is not None and len(params.tags_any) > 0:
        subquery = "".join(f" OR tags = {tag}" for tag in params.tags_any).lstrip(" OR")
        filter += f" AND ({subquery})"
    if params.authors_all is not None:
        for author in params.authors_all:
            filter += f" AND authors = {author}"
    if params.artists_all is not None:
        for artist in params.artists_all:
            filter += f" AND artist_tokens = {artist}"
    if params.seizure_warning is not None:
        filter += f" AND seizure_warning = {params.seizure_warning}"


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
            "authors",
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