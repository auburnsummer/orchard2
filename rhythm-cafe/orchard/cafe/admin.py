from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RDLevel, Club, UserProfile, ClubMembership, ClubRDLevel

# Register your models here.

admin.site.register(User, UserAdmin)

admin.site.register(RDLevel)
admin.site.register(Club)
admin.site.register(ClubMembership)
admin.site.register(ClubRDLevel)
admin.site.register(UserProfile)