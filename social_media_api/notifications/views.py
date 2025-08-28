from django.shortcuts import render
# notifications/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(
    mixins.ListModelMixin, # Allows GET (list notifications)
    mixins.RetrieveModelMixin, # Allows GET (retrieve single notification)
    mixins.UpdateModelMixin, # Allows PATCH (mark as read)
    viewsets.GenericViewSet
):
    """
    API endpoints for managing user notifications.
    - List (GET /api/notifications/): Lists notifications for the authenticated user.
    - Retrieve (GET /api/notifications/<id>/): Retrieves a specific notification.
    - Update (PATCH /api/notifications/<id>/): Marks a notification as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can access their notifications
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Ensures users can only see their own notifications.
        """
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=False, methods=['patch'])
    def mark_all_as_read(self, request):
        """
        Marks all unread notifications for the authenticated user as read.
        """
        unread_notifications = self.get_queryset().filter(is_read=False)
        unread_notifications.update(is_read=True)
        return Response({"message": "All notifications marked as read."}, status=status.HTTP_200_OK)


# Create your views here.
