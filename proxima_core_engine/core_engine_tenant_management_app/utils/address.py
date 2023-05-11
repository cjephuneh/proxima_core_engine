import logging

from django.db import DatabaseError, IntegrityError

from core_engine_tenant_management_app.models import Address
from core_engine_tenant_management_app.models import Tenant
log = logging.getLogger(__name__)


### Retrieval methods
def get_tenant_address_from_id(address_id):
    address = None
    try:
        address = Address.objects.get(address_id=address_id)
    except Address.DoesNotExist:
        log.warning("Tenant does not exist: %s", address_id)
    except Address.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple Tenants found for Tenant ID: %s", address_id)
    except Exception:
        log.exception("Tenant lookup error for Tenant ID: %s", address_id)
    
    return address



### Save methods
def save_tenant_address(**kwargs):
    """
    Create or update course entry with address_id and tenant_name
    
    Return:
    address (None if fail)
    created
    """
    # if not address_id:
    #     return None, False
    
    try:
        tenant_id = kwargs.get('tenant_id')
        billing_details_id = kwargs.get('billing_details_id')
        city = kwargs.get('city')
        country = kwargs.get('country')
        postal_code = kwargs.get('postal_code')
        state = kwargs.get('state')
        payment_number = kwargs.get('payment_number')


        address, created = Address.objects.get_or_create(
            tenant_id=Tenant.objects.get(tenant_id=tenant_id),
            billing_details_id=billing_details_id, 
            city=city,
            country=country,
            postal_code=postal_code, 
            state=state,
            payment_number=payment_number, 

        )        
        
        address.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Tenant Address save error: (Billing ID: %s, tenant_id: %s, billing_details_id: %s)",
            billing_details_id, tenant_id, billing_details_id
        )
        return None, False
    
    return address, created