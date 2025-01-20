from __future__ import annotations
import rules

from cafe.views.types import MaybeUser

@rules.predicate
def not_anonymous(user: MaybeUser):
    return user.is_authenticated