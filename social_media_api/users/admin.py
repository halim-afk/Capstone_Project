from django.contrib import admin
# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin interface for CustomUser model.
    Extends Django's default UserAdmin.
    """
    # Add custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_picture',)}),
    )
    list_display = UserAdmin.list_display + ('bio',) # Add 'bio' to list display


# ----------------------------------------------------------------------------------
# NEW APP: Posts
# Create a new app: python manage.py startapp posts
# Add 'posts' to INSTALLED_APPS in settings.py
# -----------
# Register your models here.
