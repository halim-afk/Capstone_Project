from django.contrib import admin
# follows/admin.py
from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Admin interface for the Follow model.
    Displays follower, following, and creation timestamp.
    """
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    raw_id_fields = ('follower', 'following') # Use raw ID for foreign keys for better performance with many users


# Register your models here.
