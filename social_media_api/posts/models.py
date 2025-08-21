from django.db import models
# posts/models.py
from django.db import models
from users.models import CustomUser # Import your custom user model

class Post(models.Model):
    """
    Represents a social media post created by a user.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    media = models.ImageField(upload_to='post_media/', blank=True, null=True, help_text="Optional media file (image/video).")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # To track when a post was last updated

    class Meta:
        ordering = ['-timestamp'] # Order posts by most recent first

    def __str__(self):
        return f"Post by {self.user.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

# NEW: Like Model
class Like(models.Model):
    """
    Represents a 'like' by a user on a post.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can like a post only once
        unique_together = ('user', 'post')
        ordering = ['-created_at'] # Most recent likes first

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

# NEW: Comment Model
class Comment(models.Model):
    """
    Represents a comment by a user on a post.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Oldest comments first

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"
# Create your models here.
