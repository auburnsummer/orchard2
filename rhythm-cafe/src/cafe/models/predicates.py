import rules

@rules.predicate
def not_anonymous(user):
    return user.is_authenticated