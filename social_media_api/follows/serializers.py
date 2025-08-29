# follows/serializers.py
from rest_framework import serializers
from .models import Follow
from users.serializers import UserPublicSerializer # To display public user info
from rest_framework import serializers
from .models import Follow
from users.models import CustomUser
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing Follow relationships.
    """
    follower = UserPublicSerializer(read_only=True) # Display follower's public info
    following = UserPublicSerializer(read_only=True) # Display following's public info
    following_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True, source='following'
    ) # For writing (creating follow), user provides 'following_id'

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'following_id', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at'] # Follower and created_at are set by the system

