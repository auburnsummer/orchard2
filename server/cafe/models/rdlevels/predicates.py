from __future__ import annotations
import rules
from typing import TYPE_CHECKING
from cafe.models.clubs.club import Club

if TYPE_CHECKING:
    from cafe.views.types import User
    from cafe.models.rdlevels.prefill import RDLevelPrefillResult



@rules.predicate
def can_make_level_from_prefill(user: User, prefill_result: RDLevelPrefillResult):
    # the user who initiated the prefill can create levels using it.
    if user == prefill_result.user:
        return True
    
    # an admin or owner of the club can also create levels.
    return user.has_perm("cafe.create_delegated_levels_for_club", prefill_result.club)