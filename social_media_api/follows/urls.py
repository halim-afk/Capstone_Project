# follows/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowViewSet, FeedView

router = DefaultRouter()
router.register(r'follows', FollowViewSet)


# Router for FollowViewSet (for create/destroy of follows)
router = DefaultRouter()
router.register(r'', FollowViewSet, basename='follows')

urlpatterns = [
    # Specific path for the feed
    path('feed/', FeedView.as_view(), name='feed'),
]

# Add the router URLs (for follows creation/deletion)
urlpatterns += router.urls

