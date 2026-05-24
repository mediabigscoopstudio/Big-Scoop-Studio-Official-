from core.models import NotificationRecipient


def global_notifications(request):
    if request.user.is_authenticated:

        base_qs = NotificationRecipient.objects.filter(
            user=request.user
        ).select_related('notification').order_by('-notification__created_at')

        notifications = base_qs[:10]  # slice here

        unread_count = base_qs.filter(is_read=False).count()  # filter BEFORE slice

        return {
            'global_notifications': notifications,
            'global_unread_count': unread_count
        }

    return {}