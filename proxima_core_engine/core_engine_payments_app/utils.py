import logging

import requests
from core_engine_tenant_users_app.models import Admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from .models import Payment

logger = logging.getLogger(__name__)


def build_payment_ref():
    ref = get_random_string(32)
    payments = Payment.objects.filter(merchant_ref=ref)
    if payments.exists():
        return get_random_string(32)
    return ref


def resolve_currency(from_currency: str, to_currency: str, amount: float) -> int:
    try:
        url = "https://currency-exchange.p.rapidapi.com/exchange"
        querystring = {"from": from_currency.upper(), "to": to_currency.upper()}
        headers = {
            "X-RapidAPI-Key": "332711483bmshfb97781e2645ea6p15f1fajsnf2eaafced198",
            "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code >= 400:
            return int(130 * amount)
        return int(float(response.text) * amount)
    except Exception as e:
        logger.exception(e)
        return int(130 * amount)


def get_tenant_admins(tenant):
    admins = Admin.objects.filter(tenant_id=tenant)
    return admins


def send_subscription_email(user: Admin, template_name: str):
    # TODO: (william) Better Styling
    subject = "Proxima Subscription"
    context = {'user': user}
    email_body = render_to_string(template_name=template_name, context=context)
    email = EmailMultiAlternatives(subject=subject, body=email_body,
                                   from_email='Proxima <subscription@proximaai.co>',
                                   to=[user.email])
    email.attach_alternative(content=email_body, mimetype="text/html")
    email.send()
