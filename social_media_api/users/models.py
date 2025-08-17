from django.db import models
# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser # Import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds 'bio' and 'profile_picture' fields.
    """
    bio = models.TextField(blank=True, null=True, help_text="A short biography about the user.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User's profile picture.")

    # You can add more fields here if needed later (e.g., date_of_birth, location)

    def __str__(self):
        return self.username

