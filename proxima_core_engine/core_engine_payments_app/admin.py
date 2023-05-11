from django.contrib import admin
from .models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('merchant_ref', 'transaction_id', 'complete', 'amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'complete')
    search_fields = ('merchant_ref', 'transaction_id', 'amount')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'tier', 'quota', 'is_valid', 'created_at', 'updated_at', 'expiry_date', 'cost')
    list_filter = ('created_at', 'updated_at', 'is_valid', 'tenant', 'tier', 'quota')
