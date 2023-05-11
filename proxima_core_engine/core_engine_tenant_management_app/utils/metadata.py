import logging

from django.db import DatabaseError, IntegrityError

from core_engine_tenant_management_app.models import Metadata


log = logging.getLogger(__name__)


### Retrieval methods
def get_tenant_metadata_from_id(metadata_id):
    metadata = None
    try:
        metadata = Metadata.objects.get(metadata_id=metadata_id)
    except Metadata.DoesNotExist:
        log.warning("Tenant does not exist: %s", metadata_id)
    except Metadata.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple Tenants found for Tenant ID: %s", metadata_id)
    except Exception:
        log.exception("Tenant lookup error for Tenant ID: %s", metadata_id)
    
    return metadata



### Save methods
def save_tenant_metadata(**kwargs):
    """
    Create or update course entry with metadata_id and tenant_name
    
    Return:
    metadata (None if fail)
    created
    """
    # if not metadata_id:
    #     return None, False
    
    try:
        tenant_id = kwargs.get('tenant_id')
        metadata, created = Metadata.objects.get_or_create(
            # metadata_id=metadata_id,
            tenant_id=tenant_id,
        )
        
        metadata.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Tenant Metadata save error: (tenant_id: %s)",
           tenant_id
        )
        return None, False
    
    return metadata, created