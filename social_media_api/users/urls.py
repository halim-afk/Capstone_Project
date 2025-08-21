from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserProfileViewSet

# Create a router for UserProfileViewSet
router = DefaultRouter()
router.register(r'', UserProfileViewSet, basename='users') # Register UserProfileViewSet at root of /api/users/

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]

# Add the router URLs to the urlpatterns
urlpatterns += router.urls
