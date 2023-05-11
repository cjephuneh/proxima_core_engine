import logging

from django.db import DatabaseError, IntegrityError

from core.utils.platform import get_default_platform, get_platform_from_org
from core_engine_tenant_management_app.models import Tenant


log = logging.getLogger(__name__)


### Retrieval methods
def get_tenant_from_id(tenant_id):
    tenant = None
    try:
        tenant = Tenant.objects.get(tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        log.warning("Tenant does not exist: %s", tenant_id)
    except Tenant.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple Tenants found for Tenant ID: %s", tenant_id)
    except Exception:
        log.exception("Tenant lookup error for Tenant ID: %s", tenant_id)
    
    return Tenant



### Save methods
def save_tenant(tenant_id, org=None, **kwargs):
    """
    Create or update course entry with tenant_id and tenant_name
    
    Return:
    course (None if fail)
    created
    """
    if not tenant_id:
        return None, False
    
    platform = None
    try:
        tenant, created = Tenant.objects.get_or_create(
            tenant_id=tenant_id,
            # defaults={
            #     'platform': get_default_platform()
            # }
        )
        # Retrieve platform from org if it exists, otherwise don't change
        if org:
            platform = get_platform_from_org(org)
        if platform:
            tenant.platform = platform
        
        tenant_name = kwargs.get('tenant_name')
        if tenant_name is not None:
            tenant.tenant_name = tenant_name
        
        tenant.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Tenant save error: (Tenant ID: %s, tenant_name: %s, Platform: %s)",
            tenant_id, tenant_name
        )
        return None, False
    
    return tenant, created