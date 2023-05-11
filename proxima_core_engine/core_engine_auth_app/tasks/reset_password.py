import datetime

from celery import Celery
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core_engine_auth_app.token_generator import account_activation_token
from core_engine_tenant_users_app.models import User
app = Celery("redis://")


@app.task
def send_email_to_reset_password(user_email):
    """Send Mail To Users When their account is created"""
    user = User.objects.filter(email=user_email).first()
    context = {}
    context["user_email"] = user_email
    context["url"] = settings.DOMAIN_NAME
    context["uid"] = (urlsafe_base64_encode(force_bytes(user.pk)),)
    context["token"] = default_token_generator.make_token(user)
    context["token"] = context["token"]
    context["complete_url"] = context[
        "url"
    ] + "/auth/reset-password/{uidb64}/{token}/".format(
        uidb64=context["uid"][0], token=context["token"]
    )
    subject = "Set a New Password"
    recipients = []
    recipients.append(user_email)
    html_content = render_to_string(
        "registration/password_reset_email.html", context=context
    )
    if recipients:
        msg = EmailMessage(
            subject, html_content, from_email=settings.DEFAULT_FROM_EMAIL, to=recipients
        )
        msg.content_subtype = "html"
        msg.send()
