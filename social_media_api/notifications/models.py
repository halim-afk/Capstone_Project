from django.db import models
# notifications/models.py
from django.db import models
from users.models import CustomUser
from posts.models import Post, Comment # Import Post and Comment for optional links

class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, choices=[
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('repost', 'Repost'), # Placeholder for future expansion
        ('mention', 'Mention'), # Placeholder for future expansion
    ])
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username} ({self.type}): {self.message[:50]}..."

# Create your models here.
