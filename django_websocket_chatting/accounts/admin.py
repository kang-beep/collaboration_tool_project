from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Team
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'contact', 'profile_picture', 'teams')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'contact', 'profile_picture', 'teams')}),
    )

admin.site.register(CustomUser)
admin.site.register(Team)
