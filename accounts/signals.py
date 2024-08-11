from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserHistory

@receiver(user_logged_in)
def save_login_history(sender, user, request, **kwargs):
    UserHistory.objects.create(user=user, history_data='Uživatel se přihlásil')
