# posts/serializers.py
from rest_framework import serializers
from .models import Post, Like, Comment # NEW: Import Like and Comment
from users.serializers import UserPublicSerializer # To show public user info in post


# NEW: Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    user = UserPublicSerializer(read_only=True) # Display public user info for the commenter

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'post', 'created_at', 'updated_at'] # These fields are set by system/URL

    def create(self, validated_data):
        # 'post' and 'user' will be set by the view's perform_create method
        return Comment.objects.create(**validated_data)


# NEW: Like Serializer (used primarily for creation/deletion)
class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    Used for creating and confirming likes.
    """
    user = UserPublicSerializer(read_only=True) # Display public user info for the liker

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at'] # All fields set by system/URL


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    Handles creation, viewing, updating of posts.
    Includes likes_count and comments_count.
    """
    user = UserPublicSerializer(read_only=True) # Display public user info, not writable
    media = serializers.ImageField(required=False, allow_null=True) # Make media optional
    likes_count = serializers.SerializerMethodField() # NEW: Field to show total likes
    comments_count = serializers.SerializerMethodField() # NEW: Field to show total comments
    # Optional: nested comments (can be complex for large numbers of comments)
    # comments = CommentSerializer(many=True, read_only=True) # NEW: Nested comments

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'media', 'timestamp', 'updated_at',
                  'likes_count', 'comments_count'] # NEW: Added counts
        read_only_fields = ['id', 'user', 'timestamp', 'updated_at', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count() # Counts related likes

    def get_comments_count(self, obj):
        return obj.comments.count() # Counts related comments

    def create(self, validated_data):
        """
        Automatically sets the user to the current authenticated user on creation.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_content(self, value):
        """
        Ensure content is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        return value