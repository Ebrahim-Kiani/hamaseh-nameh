from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework import status

from .generate_active_code import generate_activate_code
from django.http import JsonResponse


def send_email(to_email, template_name, context, subject):
    try:
        html_message = render_to_string(template_name, context)
        plain_text = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER

        sent = send_mail(subject, plain_text, from_email, [to_email], html_message=html_message)
        if sent == 1:
            return True

    except Exception as error:
        print(f"Error sending activation email: {str(error)}")
    return False



def send_activation_email(user, template_name, subject, host, scheme):
    user = user
    user_active_code = generate_activate_code(user)

    context = {
        'user_active_code': user_active_code,
        'host': host,
        'scheme': scheme
    }
    to_email = user.email
    send_email(to_email, template_name, context, subject)


def expiretime_validator(user):
    expire_time = timedelta(minutes=settings.EMAIL_EXPIRETIME)

    difference_time = timezone.now() - user.activation_code_expiration

    if expire_time > difference_time:
        return False
    else:
        return True
