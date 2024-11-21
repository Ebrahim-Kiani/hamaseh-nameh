from datetime import timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings



def generate_activate_code(user):
    user.email_active_code = get_random_string(72)
    user.activation_code_expiration = timezone.now() + timedelta(minutes=settings.EMAIL_EXPIRETIME)
    user.save()
    return user.email_active_code
