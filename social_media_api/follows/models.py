from django.db import models
# follows/models.py
from django.db import models
from users.models import CustomUser # Import your custom user model

class Follow(models.Model):
    """
    Represents a follow relationship between two users.
    'follower' is the user initiating the follow.
    'following' is the user being followed.
    """
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_relationships')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_relationships')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures that a user can only follow another user once
        unique_together = ('follower', 'following')
        ordering = ['-created_at'] # Most recent follows first

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


# Create your models here.
