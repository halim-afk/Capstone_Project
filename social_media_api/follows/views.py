from django.shortcuts import render
# follows/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError # For custom validation errors
from rest_framework.generics import ListAPIView # For the feed
from django.db.models import Q # Import Q for feed filtering (optional stretch goal)
from .models import Follow
from users.models import CustomUser # Import CustomUser to filter users for feed
from posts.models import Post # Import Post to get posts for the feed
from posts.serializers import PostSerializer # To serialize posts for the feed
from notifications.models import Notification # NEW: Import Notification model
from .serializers import FollowSerializer  
# ViewSet for Follow operations (Create/Destroy)
class FollowViewSet(
    mixins.CreateModelMixin, # Allows POST (create)
    mixins.DestroyModelMixin, # Allows DELETE
    mixins.ListModelMixin, # Allows GET (list of follows) - useful for seeing who user follows
    viewsets.GenericViewSet
):
    """
    API endpoints for managing follow relationships.
    - Create (POST /api/follows/): Authenticated user follows another user.
    - Destroy (DELETE /api/follows/<id>/): Authenticated user unfollows a relationship they initiated.
    - List (GET /api/follows/): Authenticated user can see their own followings.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated] # Requires authentication for all follow actions
    lookup_field = 'pk' # Use primary key for lookup (e.g., to delete a specific follow record)

    def get_queryset(self):
        """
        Ensures users can only see/delete their own follow relationships.
        """
        return self.queryset.filter(follower=self.request.user)

    def perform_create(self, serializer):
        """
        Sets the follower to the current authenticated user.
        Prevents self-following and duplicate follows.
        """
        following_user = serializer.validated_data.get('following')
        if self.request.user == following_user:
            raise ValidationError("You cannot follow yourself.")

        # Check for existing follow to prevent duplicates before unique_together handles it
        if Follow.objects.filter(follower=self.request.user, following=following_user).exists():
            raise ValidationError("You are already following this user.")

        follow_instance = serializer.save(follower=self.request.user) # Set the follower to the current user

        # NEW: Create a notification for the followed user
        Notification.objects.create(
            recipient=following_user,
            sender=self.request.user,
            type='follow',
            message=f"{self.request.user.username} started following you."
        )

        return follow_instance


    def perform_destroy(self, instance):
        """
        Deletes the follow relationship.
        """
        follower_username = instance.follower.username
        following_username = instance.following.username
        instance.delete()
        return Response(
            {"message": f"{follower_username} unfollowed {following_username} successfully."},
            status=status.HTTP_200_OK
        )


class FeedView(ListAPIView):
    """
    API endpoint for viewing a personalized feed of posts from followed users.
    Requires authentication.
    Posts are ordered in reverse chronological order.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None # Use default pagination from settings.py or define custom

    def get_queryset(self):
        """
        Retrieves posts from users the current user is following,
        ordered by timestamp (most recent first).
        """
        user = self.request.user
        # Get IDs of users that the current user is following
        followed_users_ids = user.following_relationships.values_list('following__id', flat=True)

        # Filter posts where the author's ID is in the list of followed users' IDs
        # and order by timestamp
        queryset = Post.objects.filter(user__id__in=followed_users_ids).order_by('-timestamp')

        # Optional: Implement filtering by date or search by keyword (Stretch Goal)
        query = self.request.GET.get('q')
        date_param = self.request.GET.get('date')

        if query:
            queryset = queryset.filter(
                Q(content__icontains=query) | Q(user__username__icontains=query)
            ).distinct() # Use distinct to avoid duplicate posts if they match multiple criteria

        if date_param:
            try:
                # Assuming date_param is in 'YYYY-MM-DD' format
                from datetime import datetime
                target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(timestamp__date=target_date)
            except ValueError:
                # Handle invalid date format if needed, perhaps log or return a specific error
                pass # For now, just ignore if date format is bad

        return queryset

# Create your views here.
