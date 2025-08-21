from django.shortcuts import render
# users/views.py

from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token # For token-based authentication
from rest_framework.permissions import AllowAny, IsAuthenticated # Import permissions
from django.contrib.auth import authenticate, login, logout # Django's built-in auth functions

from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserPublicSerializer
from .permissions import IsOwnerOrReadOnly # Import your custom permission

# API for User Registration
class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows any user to register.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Anyone can register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user) # Generate token for new user
        return Response({
            "message": "User registered successfully",
            "user_id": user.id,
            "username": user.username,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# API for User Login
class UserLoginView(views.APIView):
    """
    API endpoint for user login.
    Authenticates user and returns an authentication token.
    """
    permission_classes = [AllowAny] # Anyone can attempt to login

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            # login(request, user) # Optional: Use Django's session login if SessionAuthentication is enabled
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id, "username": user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# API for User Logout
class UserLogoutView(views.APIView):
    """
    API endpoint for user logout.
    Deletes the user's authentication token.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated] # Only logged-in users can logout

    def post(self, request, *args, **kwargs):
        # Delete the user's current authentication token
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        # logout(request) # Optional: Clear Django's session if SessionAuthentication is used
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


# ViewSet for User Profile CRUD operations
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoints for viewing, updating, and deleting user profiles.
    - List (GET /api/users/): Public, but only shows basic public info.
    - Retrieve (GET /api/users/<id>/): Public, shows basic public info.
    - Update (PUT/PATCH /api/users/<id>/): Authenticated, owner-only.
    - Destroy (DELETE /api/users/<id>/): Authenticated, owner-only.
    - Create is handled by UserRegisterView separately.
    """
    queryset = CustomUser.objects.all()
    lookup_field = 'pk' # Ensures URLs use primary key

    def get_serializer_class(self):
        """
        Returns different serializers based on the action (e.g., public view vs. owner's profile edit).
        """
        if self.action in ['retrieve', 'list']:
            # For public viewing of user profiles
            return UserPublicSerializer
        # For update/partial_update (user editing their own profile)
        return UserProfileSerializer

    def get_permissions(self):
        """
        Sets permissions based on the action being performed.
        - Public (AllowAny) for list and retrieve.
        - Owner-only (IsAuthenticated, IsOwnerOrReadOnly) for update and destroy.
        """
        if self.action in ['retrieve', 'list']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            # Default to IsAuthenticated for any other unexpected action
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        """
        Handles user account deletion.
        """
        username = instance.username # Get username before deleting
        instance.delete()
        # No 204 No Content for DRF DefaultRouter delete method as per common practice
        return Response({"message": f"User {username} and all associated data deleted successfully."}, status=status.HTTP_200_OK)


# Create your views here.
