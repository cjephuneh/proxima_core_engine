from django.conf import settings
from django.shortcuts import reverse

from .models import Payment
from .utils import build_payment_ref, resolve_currency
import json
import requests

from core_engine_tenant_management_app.models import Tenant


def build_payment_uri(request, tenant_id) -> str:
    tenant = Tenant.objects.get(tenant_id=tenant_id)
    subscription = tenant.subscription
    tier, quota = subscription.tier, subscription.quota
    amount = resolve_currency('USD', 'KES', subscription.cost)
    p = Payment.objects.create(merchant_ref=build_payment_ref(), amount=amount, subscription=subscription)
    payment_opts = 'account, card, banktransfer mpesa'
                   
    payment_url = "https://api.flutterwave.com/v3/payments"

    payload = json.dumps({
        "tx_ref": f"{p.merchant_ref}",
        "amount": f"{amount}",
        "currency": "KES",
        "redirect_url": request.build_absolute_uri(reverse('core_engine_payments_app:callback')),
        "payment_options": payment_opts,
        "customer": {
            "email": f"{tenant.tenant_email}",
            "phonenumber": f"{tenant.tenant_phone}",
            "name": f"{tenant.tenant_name}"
        },
        "customizations": {
            "title": "Proxima",
            "description": f"{quota} {tier} Proxima Subscription",
            "logo": "https://www.proximaai.co/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fkosselogo.697eb949.png&w=150&q=150"
        }
    })
    headers = {
        'Authorization': f'Bearer {settings.FW_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url=payment_url, headers=headers, data=payload)
    return response.json()['data']['link']
