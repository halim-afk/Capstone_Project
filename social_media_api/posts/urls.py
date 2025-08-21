from rest_framework.routers import DefaultRouter
from django.urls import path, include # NEW: include for nested routes if desired
from .views import PostViewSet, CommentViewSet # NEW: Import CommentViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename='posts') # Main posts endpoints
router.register(r'comments', CommentViewSet, basename='comments') # NEW: Top-level comments endpoint

# Define specific URLs for post-related actions (like, unlike, add comment)
urlpatterns = [
    # Custom actions for PostViewSet
    path('<int:pk>/like/', PostViewSet.as_view({'post': 'like_post'}), name='post-like'),
    path('<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike_post'}), name='post-unlike'),
    path('<int:pk>/comments/', PostViewSet.as_view({'post': 'add_comment', 'get': 'recent_comments'}), name='post-comments'),
    # You can also define specific paths for comment creation like this if you want:
    # path('<int:post_pk>/comments/new/', CommentViewSet.as_view({'post': 'create'}), name='post-comment-create'),
]

# Add the router URLs (for all Post and top-level Comment CRUD)
urlpatterns += router.urls


# ----------------------------------------------------------------------------------
# NEW APP: Follows
# Create a new app: python manage.py startapp follows
# Add 'follows' to INSTALLED_APPS in settings.py
# ----------------------------------------------------------------------------------
