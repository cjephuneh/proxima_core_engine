import logging

from django.db import DatabaseError, IntegrityError

from core_engine_social_intergtaions.models import FaceBookIntergration
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_tenant_facebook_intergration(tenant_id):
    facebook_intergration = None
    try:
        facebook_intergration = FaceBookIntergration.objects.get(tenant_id=tenant_id)
    except FaceBookIntergration.DoesNotExist:
        log.warning("facebook_intergration does not exist: %s", tenant_id)
    except FaceBookIntergration.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple facebook_intergrations found for tenant ID: %s", tenant_id)
    except Exception:
        log.exception("facebook_intergration lookup error for tenant ID: %s", tenant_id)
    
    return facebook_intergration



### Save methods
def save_tenant_facebook_intergrations( **kwargs):
    """
    Create Tenant facebook intergration
    
    Return:
    facebook inergration
    created
    """    
    facebook_intergration = None
    try:
        tenant_id = kwargs.get('tenant_id')
        facebook_intergration, created = FaceBookIntergration.objects.get_or_create(
            tenant_id=tenant_id
        )
        facebook_intergration.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "facebook Intergration save error: (tenant id: %s)",
            tenant_id
        )
        return None, False
    return facebook_intergration, created


def update_tenant_facebook_intergrations(**kwargs):
    """
    Update Tenant Facebook Integration
    
    Return:
    - Updated Facebook Integration (None if fail)
    - is_updated
    """
    tenant_id = kwargs.get('tenant_id')

    try:
        facebook_intergration = FaceBookIntergration.objects.get(tenant_id=tenant_id)
        
        # Update the attributes of the facebook_intergration object based on the kwargs
        for key, value in kwargs.items():
            setattr(facebook_intergration, key, value)
        
        # Save the updated facebook_intergration object
        facebook_intergration.save()
        
        return facebook_intergration, True

    except (FaceBookIntergration.DoesNotExist, IntegrityError, DatabaseError) as e:
        log.error("Error updating Facebook Integration: %s", str(e))
        return None, False
