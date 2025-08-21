from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles creating a new user, including hashing the password.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        """
        Check that password and password2 are the same.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        """
        Create and return a new `CustomUser` instance, given the validated data.
        """
        # Remove password2 before creating the user
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profiles.
    Excludes password for security.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'date_joined'] # These fields are not directly editable via profile update


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for public user profiles (e.g., when viewing another user's profile).
    Excludes sensitive information like email and bio for privacy by default.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_picture']
        read_only_fields = ['id', 'username', 'profile_picture']
