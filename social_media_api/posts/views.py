from django.shortcuts import render
# posts/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsOwnerOrReadOnly # Import the custom permission
from rest_framework.decorators import action # NEW: For custom actions on ViewSets
from rest_framework.exceptions import ValidationError # NEW: For specific validation errors

from .models import Post, Like, Comment # NEW: Import Like and Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer # NEW: Import new serializers

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing posts.
    - List (GET /api/posts/): Publicly accessible, lists all posts.
    - Create (POST /api/posts/): Authenticated users only.
    - Retrieve (GET /api/posts/<id>/): Publicly accessible, view single post.
    - Update (PUT/PATCH /api/posts/<id>/): Authenticated, owner-only.
    - Destroy (DELETE /api/posts/<id>/): Authenticated, owner-only.
    - Custom actions for Liking/Unliking, and managing comments on posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk' # Use primary key for lookup

    def get_permissions(self):
        """
        Sets permissions based on the action.
        - List and Retrieve are public (AllowAny).
        - Create requires authentication (IsAuthenticated).
        - Update and Destroy require authentication and ownership (IsAuthenticated, IsOwnerOrReadOnly).
        - Custom actions for likes/comments might have their own permissions.
        """
        if self.action in ['list', 'retrieve', 'recent_comments']: # 'recent_comments' for public read
            permission_classes = [AllowAny]
        elif self.action in ['create', 'like_post', 'unlike_post', 'add_comment']: # Actions requiring authentication
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated] # Default for any other action
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user as the author of the post.
        """
        serializer.save(user=self.request.user) # Set the user (author) field

    def perform_destroy(self, instance):
        """
        Deletes the post.
        """
        post_id = instance.id
        instance.delete()
        return Response({"message": f"Post {post_id} deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like_post(self, request, pk=None):
        """
        API endpoint to like a specific post.
        """
        post = self.get_object() # Get the post instance
        user = request.user

        # Check if user already liked the post
        if Like.objects.filter(post=post, user=user).exists():
            raise ValidationError("You have already liked this post.")

        Like.objects.create(post=post, user=user)
        return Response({"message": "Post liked successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike_post(self, request, pk=None):
        """
        API endpoint to unlike a specific post.
        """
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(post=post, user=user)
        if not like.exists():
            raise ValidationError("You have not liked this post.")

        like.delete()
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        """
        API endpoint to add a comment to a specific post.
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post) # Set user and post for the comment
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def recent_comments(self, request, pk=None):
        """
        API endpoint to list recent comments on a specific post.
        Publicly accessible.
        """
        post = self.get_object()
        comments = post.comments.all().order_by('-created_at')[:5] # Get 5 most recent comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# NEW: Comment ViewSet for CRUD on comments themselves (editing/deleting a specific comment)
class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing comments.
    - List: Not provided directly via ViewSet, typically nested under posts.
    - Retrieve (GET /api/comments/<id>/): Publicly accessible.
    - Update (PUT/PATCH /api/comments/<id>/): Authenticated, owner-only.
    - Destroy (DELETE /api/comments/<id>/): Authenticated, owner-only.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # Default permissions

    def get_permissions(self):
        """
        Sets permissions for comment actions.
        - Retrieve is public.
        - Update and Destroy require authentication and ownership.
        """
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else: # For create, list (if exposed), etc.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # This will primarily be used if creating comments via a direct endpoint.
        # For creating comments from a post's page, PostViewSet's add_comment is used.
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        comment_id = instance.id
        instance.delete()
        return Response({"message": f"Comment {comment_id} deleted successfully."}, status=status.HTTP_200_OK)
# Create your views here.
