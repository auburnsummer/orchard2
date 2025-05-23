from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

from .models.clubs.club import Club
from .models.clubs.club_membership import ClubMembership
from .models.clubs.club_invite import ClubInvite
from .models.discord_guild import DiscordGuild
from .models.rdlevels.prefill import RDLevelPrefillResult
from .models.rdlevels.rdlevel import RDLevel
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

admin.site.register(Club, SimpleHistoryAdmin)
admin.site.register(ClubMembership)
admin.site.register(ClubInvite)
admin.site.register(DiscordGuild)
admin.site.register(RDLevelPrefillResult)
admin.site.register(RDLevel, SimpleHistoryAdmin)