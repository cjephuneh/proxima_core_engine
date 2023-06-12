import logging

from django.db import DatabaseError, IntegrityError

from core_engine_social_intergtaions.models import WhatsAppIntergration
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_tenant_whatsapp_intergration(tenant_id):
    whatsapp_intergration = None
    try:
        whatsapp_intergration = WhatsAppIntergration.objects.get(tenant_id=tenant_id)
    except WhatsAppIntergration.DoesNotExist:
        log.warning("whatsapp_intergration does not exist: %s", tenant_id)
    except WhatsAppIntergration.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple whatsapp_intergrations found for tenant ID: %s", tenant_id)
    except Exception:
        log.exception("whatsapp_intergration lookup error for tenant ID: %s", tenant_id)
    
    return whatsapp_intergration



### Save methods
def save_tenant_whatsapp_intergrations( **kwargs):
    """
    Create Tenant WhatsApp intergration
    
    Return:
    WhatsApp inergration
    created
    """
    # if not whatsapp_intergration_id:
    #     return None, False
    
    whatsapp_intergration = None
    try:
        tenant_id = kwargs.get('tenant_id')

        whatsapp_intergration, created = WhatsAppIntergration.objects.get_or_create(
            tenant_id=tenant_id

        )
        
        whatsapp_intergration.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "WhatsApp Intergration save error: (tenant id: %s)",
            tenant_id
        )
        return None, False
    
    return whatsapp_intergration, created


def update_tenant_whatsapp_intergrations(**kwargs):
    """
    Update Tenant whatsapp Integration
    
    Return:
    - Updated whatsapp Integration (None if fail)
    - is_updated
    """
    tenant_id = kwargs.get('tenant_id')

    try:
        whatsapp_intergration = WhatsAppIntergration.objects.get(tenant_id=tenant_id)
        
        # Update the attributes of the whatsapp_intergration object based on the kwargs
        for key, value in kwargs.items():
            setattr(whatsapp_intergration, key, value)
        
        # Save the updated whatsapp_intergration object
        whatsapp_intergration.save()
        
        return whatsapp_intergration, True

    except (WhatsAppIntergration.DoesNotExist, IntegrityError, DatabaseError) as e:
        log.error("Error updating whatsapp Integration: %s", str(e))
        return None, False