from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List, Dict, Any, Union

from django_bridge.response import Response

from cafe.views.types import HttpRequest

from cafe.management.commands.setuptypesense import get_typesense_client, RDLEVEL_ALIAS_NAME
from cafe.models import RDLevel

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
    facet_query_field: Optional[str]
    facet_query: Optional[str]


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
        "approved": ApprovalSearchOptions.APPROVED_ONLY,
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

    facet_query = request.GET.get('facet_query', None)
    facet_query_field = request.GET.get('facet_query_field', None)
    
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
        seizure_warning=seizure_warning,
        facet_query=facet_query,
        facet_query_field=facet_query_field
    )

def get_typesense_filter_query(params: SearchLevelParams) -> str:
    parts = []
    if params.approval == ApprovalSearchOptions.APPROVED_ONLY:
        parts.append("approval:>=10")
    elif params.approval == ApprovalSearchOptions.PENDING:
        parts.append("approval:=0")
    elif params.approval == ApprovalSearchOptions.REJECTED_ONLY:
        parts.append("approval:<0")

    if params.min_bpm is not None or params.max_bpm is not None:
        if params.min_bpm is not None:
            parts.append(f"min_bpm:>={params.min_bpm}")
        if params.max_bpm is not None:
            parts.append(f"max_bpm:<={params.max_bpm}")

    if params.difficulties:
        parts.append(f"difficulty:=[{','.join(map(str, params.difficulties))}]")

    bool_params = [
        ("single_player", params.single_player),
        ("two_player", params.two_player),
        ("has_classics", params.has_classics),
        ("has_oneshots", params.has_oneshots),
        ("has_squareshots", params.has_squareshots),
        ("has_freezeshots", params.has_freezeshots),
        ("has_freetimes", params.has_freetimes),
        ("has_holds", params.has_holds),
        ("has_window_dance", params.has_window_dance),
        ("seizure_warning", params.seizure_warning)
    ]

    for param_name, param_value in bool_params:
        if param_value is not None:
            parts.append(f"{param_name}:={str(param_value).lower()}")

    if params.tags_all:
        for tag in params.tags_all:
            parts.append(f"tags:={tag}")
    if params.tags_any:
        parts.append(f"tags:=[{','.join(params.tags_any)}]")

    if params.authors_all:
        for author in params.authors_all:
            parts.append(f"authors:={author}")
    if params.artists_all:
        for artist in params.artists_all:
            parts.append(f"artist_tokens:={artist}")

    return " && ".join(parts)

def search_levels(request: HttpRequest):
    params = get_search_params(request)
    offset = (params.page - 1) * RESULTS_PER_PAGE

    filter_opts = {
        "q": params.q,
        "query_by": "song,song_alt,artist_tokens,authors,description,tags",
        "query_by_weights": "10,10,8,8,6,6",
        "filter_by": get_typesense_filter_query(params),
        "offset": offset,
        "limit": RESULTS_PER_PAGE + 1,
        "facet_by": "artist_tokens,tags,authors,difficulty,single_player,two_player,has_classics,has_oneshots,has_squareshots,has_freezeshots,has_freetimes,has_holds,has_window_dance,submitter.id,club.id",
        "include_fields": "id",
        "sort_by": "_text_match:desc"
    }

    if params.facet_query and params.facet_query_field:
        filter_opts['facet_query'] = f"{params.facet_query_field}:{params.facet_query}"

    typesense_client = get_typesense_client()
    search_results = typesense_client.collections[RDLEVEL_ALIAS_NAME].documents.search(filter_opts)

    # this is fine! https://www.sqlite.org/np1queryprob.html
    levels = [
        RDLevel.objects.get(id=level_id).to_dict()
        for level_id in (
            hit['document']['id'] for hit in search_results['hits']
        )
    ]

    facet_distribution = {}
    for facet in search_results['facet_counts']:
        facet_distribution[facet['field_name']] = facet['counts']

    if params.facet_query and params.facet_query_field:
        return Response(request, request.resolver_match.view_name, {
            "facets": facet_distribution[params.facet_query_field]
        })

    return Response(request, request.resolver_match.view_name, {
        "results": {
            "hits": levels,
            "estimatedTotalHits": search_results['found'],
            "processingTimeMs": search_results['search_time_ms'],
            "limit": RESULTS_PER_PAGE,
            "offset": offset,
            "query": params.q,
            "facetDistribution": facet_distribution
        }
    })