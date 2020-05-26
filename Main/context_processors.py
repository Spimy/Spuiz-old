from .models import Notification

def has_notifications(request):

    if request.user.is_authenticated:
    
        has_notification = False   
        notifications = Notification.objects.filter(for_user=request.user)
        
        for notification in notifications:
            if not notification.read:
                has_notification = True
                break
    
        return {"has_notification": has_notification}
    
    else:
        return {"has_notification": False}