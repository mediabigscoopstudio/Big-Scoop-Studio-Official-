# core/views.py

from django.http import JsonResponse
from core.models import NotificationRecipient


def mark_notification_read(request, notif_id):
    try:
        notif = NotificationRecipient.objects.get(id=notif_id, user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({'status': 'ok'})
    except:
        return JsonResponse({'status': 'error'})
    
def mark_all_notifications(request):
    if request.user.is_authenticated:
        NotificationRecipient.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})