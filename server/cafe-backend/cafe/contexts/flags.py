from waffle.models import AbstractUserFlag
from django.db.models import QuerySet
from waffle import get_waffle_flag_model, flag_is_active
from cafe.views.types import HttpRequest

Flag = get_waffle_flag_model()

def flags(request: HttpRequest):
    flags: QuerySet[AbstractUserFlag, AbstractUserFlag] = Flag.objects.all()
    result = {}
    for flag in flags:
        result[flag.name] = flag_is_active(request, flag.name)
    return result