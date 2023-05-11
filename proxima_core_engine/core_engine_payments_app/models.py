from dateutil import relativedelta
from django.db import models
from django.db.models.signals import post_save

from core_engine_tenant_management_app.models import Tenant


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Payment(TimestampModel):
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    merchant_ref = models.CharField(max_length=32, unique=True)
    transaction_id = models.CharField(max_length=128, null=True, blank=True)
    amount = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)
    payload = models.JSONField(null=True, blank=True)
    payment_payload = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.merchant_ref


class Subscription(TimestampModel):
    TIERS = (
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    )
    QUOTAS = (
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('BiAnnally', 'BiAnnally'),
        ('Annually', 'Annually'),
    )

    QUOTA_DURATIONS = {
        'Monthly': 1,
        'Quarterly': 3,
        'BiAnnually': 6,
        'Annually': 12
    }
    TIER_PRICES = {
        'Basic': 10,
        'Standard': 20,
        'Premium': 30,
    }

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    tier = models.CharField(max_length=16, default='Basic', choices=TIERS)
    quota = models.CharField(max_length=16, default='Monthly', choices=QUOTAS)
    is_valid = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        return super(Subscription, self).save(*args, **kwargs)

    @property
    def is_basic(self):
        return self.tier == 'Basic'

    @property
    def is_standard(self):
        return self.tier == 'Standard'

    @property
    def is_premium(self):
        return self.tier == 'Premium'

    @property
    def cost(self):
        return self.QUOTA_DURATIONS[self.quota] * self.TIER_PRICES[self.tier]

    def set_expiry_date(self):
        self.expiry_date = self.created_at + relativedelta.relativedelta(
            months=self.QUOTA_DURATIONS[self.quota]
        )
        self.save()


def create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.get_or_create(
            tenant=instance
        )


post_save.connect(create_subscription, sender=Tenant)
