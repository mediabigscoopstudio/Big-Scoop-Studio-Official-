from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from core.models import Notification, NotificationRecipient


def send_notification(users, title, message):

    channel_layer = get_channel_layer()

    notification = Notification.objects.create(
        title=title,
        message=message
    )

    for user in users:

        NotificationRecipient.objects.create(
            notification=notification,
            user=user
        )

        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_notification",
                "title": title,
                "message": message,
            }
        )