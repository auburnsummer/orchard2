from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
from .models import User

from .models.clubs.club import Club
from .models.clubs.club_membership import ClubMembership
from .models.clubs.club_invite import ClubInvite
from .models.discord_guild import DiscordGuild
from .models.rdlevels.prefill import RDLevelPrefillResult
from .models.rdlevels.rdlevel import RDLevel
from .models.rdlevels.daily_blend import DailyBlend
from simple_history.admin import SimpleHistoryAdmin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('id', 'display_name', 'email', 'is_staff', 'is_superuser')
    fieldsets = DjangoUserAdmin.fieldsets+ (
        (                      
            None, # you can also use None 
            {
                'fields': (
                    'display_name',
                    'id'
                ),
            },
        ),
    )
    search_fields = ('display_name', 'email')

admin.site.register(Club, SimpleHistoryAdmin)
admin.site.register(ClubMembership)
admin.site.register(ClubInvite)
admin.site.register(DiscordGuild)
admin.site.register(RDLevelPrefillResult)
admin.site.register(RDLevel, SimpleHistoryAdmin)
admin.site.register(DailyBlend)
admin.site.register(DailyBlendRandomPool)