import logging

from django.db import DatabaseError, IntegrityError

from core_engine_subscriptions_app.models import Coupon 
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_tenant_coupon_from_id(coupon_id):
    coupon = None
    try:
        coupon = Coupon.objects.get(coupon_id=coupon_id)
    except Coupon.DoesNotExist:
        log.warning("coupon does not exist: %s", coupon_id)
    except Coupon.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple coupons found for coupon ID: %s", coupon_id)
    except Exception:
        log.exception("coupon lookup error for coupon ID: %s", coupon_id)
    
    return coupon



### Save methods
def save_tenant_coupon(coupon_id, org=None, **kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    anonymoususer (None if fail)
    created
    """
    if not coupon_id:
        return None, False
    
    coupon = None
    try:
        stripe_coupon_id = kwargs.get('stripe_coupon_id')
        valid = kwargs.get('valid')
        amount_off = kwargs.get('amount_off')
        currency = kwargs.get('currency')
        duration = kwargs.get('duration')
        duration_in_months = kwargs.get('duration_in_months')
        max_redemptions = kwargs.get('max_redemptions')
        redeem_by = kwargs.get('redeem_by')
        times_redeemed = kwargs.get('times_redeemed')
        discount_id = kwargs.get('discount_id')

        coupon, created = Coupon.objects.get_or_create(
            coupon_id=coupon_id,
            stripe_coupon_id=stripe_coupon_id,
            valid=valid,
            amount_off=amount_off,
            currency=currency,
            duration=duration,
            duration_in_months=duration_in_months,
            max_redemptions=max_redemptions,
            redeem_by=redeem_by,
            times_redeemed=times_redeemed,
            discount_id=discount_id

        )
        
        
        coupon.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Coupon user save error: (stripe_coupon_id: %s, stripe_coupon_id: %s)",
            coupon_id, stripe_coupon_id
        )
        return None, False
    
    return coupon, created