# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from users.serializers import UserPublicSerializer # To display public user info
from posts.serializers import PostSerializer, CommentSerializer # To link related objects in notifications

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    Includes related sender, post, and comment information.
    """
    recipient = UserPublicSerializer(read_only=True)
    sender = UserPublicSerializer(read_only=True)
    post = PostSerializer(read_only=True) # Nested post details
    comment = CommentSerializer(read_only=True) # Nested comment details

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'post', 'comment', 'type', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'recipient', 'sender', 'post', 'comment', 'type', 'message', 'created_at']

