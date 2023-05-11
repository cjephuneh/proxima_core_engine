from celery import shared_task
from django.utils import timezone
from python_flutterwave import payment

from .models import Payment, Subscription
from .utils import get_tenant_admins, send_subscription_email


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def resolve_payments():
    payments = Payment.objects.filter(complete=False, transaction_id__isnull=False)
    if payments.exists():
        for p in payments:
            details = payment.get_payment_details(p.transaction_id)
            p.payload = details
            if details['data']['status'] == 'successful':
                p.complete = True
                p.subscription.is_valid = True
                p.subscription.set_expiry_date()
            if details['data']['status'] != 'successful':
                p.complete = False
                p.subscription.is_valid = False
                p.subscription.save()
                admins = get_tenant_admins(tenant=p.subscription.tenant)
                for admin in admins:
                    send_subscription_email(
                        user=admin,
                        template_name='core_engine_payments_app/emails/subscription_problem.html'
                    )
            p.save()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def cleanup_payments():
    payments = Payment.objects.filter(complete=False, transaction_id__isnull=True)
    payments.delete()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def watch_subscriptions():
    subscriptions = Subscription.objects.filter(is_valid=True)
    if subscriptions.exists():
        for sub in subscriptions:
            admins = get_tenant_admins(tenant=sub.tenant)
            if sub.expiry_date < timezone.now():
                sub.is_valid = False
                sub.save()
                for admin in admins:
                    send_subscription_email(
                        user=admin,
                        template_name='core_engine_payments_app/emails/subscription_expiry.html'
                    )
