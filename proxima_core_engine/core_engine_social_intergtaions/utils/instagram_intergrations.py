import logging

from django.db import DatabaseError, IntegrityError

from core_engine_social_intergtaions.models import InstagramIntergration
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_tenant_instagram_intergration(tenant_id):
    instagram_intergration = None
    try:
        instagram_intergration = InstagramIntergration.objects.get(tenant_id=tenant_id)
    except InstagramIntergration.DoesNotExist:
        log.warning("instagram_intergration does not exist: %s", tenant_id)
    except InstagramIntergration.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple instagram_intergrations found for tenant ID: %s", tenant_id)
    except Exception:
        log.exception("instagram_intergration lookup error for tenant ID: %s", tenant_id)
    
    return instagram_intergration



### Save methods
def save_tenant_instagram_intergrations( **kwargs):
    """
    Create Tenant instagram intergration
    
    Return:
    instagram inergration
    created
    """    
    instagram_intergration = None
    try:
        tenant_id = kwargs.get('tenant_id')
        instagram_intergration, created = InstagramIntergration.objects.get_or_create(
            tenant_id=tenant_id
        )
        instagram_intergration.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "instagram Intergration save error: (tenant id: %s)",
            tenant_id
        )
        return None, False
    return instagram_intergration, created


def update_tenant_instagram_intergrations(**kwargs):
    """
    Update Tenant instagram Integration
    
    Return:
    - Updated instagram Integration (None if fail)
    - is_updated
    """
    tenant_id = kwargs.get('tenant_id')

    try:
        instagram_intergration = InstagramIntergration.objects.get(tenant_id=tenant_id)
        
        # Update the attributes of the instagram_intergration object based on the kwargs
        for key, value in kwargs.items():
            setattr(instagram_intergration, key, value)
        
        # Save the updated instagram_intergration object
        instagram_intergration.save()
        
        return instagram_intergration, True

    except (InstagramIntergration.DoesNotExist, IntegrityError, DatabaseError) as e:
        log.error("Error updating instagram Integration: %s", str(e))
        return None, False
