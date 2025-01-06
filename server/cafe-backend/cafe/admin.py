from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('id', 'display_name', 'email', 'is_staff', 'is_superuser')
    fieldsets = DjangoUserAdmin.fieldsets+ (
        (                      
            None, # you can also use None 
            {
                'fields': (
                    'display_name',
                ),
            },
        ),
    )
