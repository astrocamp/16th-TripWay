from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notify_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifies/notify_list.html', {'notifications': notifications})

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})
