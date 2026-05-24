from django.db import models
from core.models.users import User


class Notification(models.Model):

    title = models.CharField(max_length=255)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class NotificationRecipient(models.Model):

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='recipients'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_notifications'
    )

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} → {self.notification.title}"