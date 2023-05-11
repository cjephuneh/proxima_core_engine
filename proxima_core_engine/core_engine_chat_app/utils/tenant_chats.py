import logging

from django.db import DatabaseError, IntegrityError

from core_engine_chat_app.models import TenantChats
# save_anonymous_user

log = logging.getLogger(__name__)


### Retrieval methods
def get_tenant_chat_from_id(tenant_chats_id):
    tenantchats = None
    try:
        tenantchats = TenantChats.objects.get(tenant_chats_id=tenant_chats_id)
    except TenantChats.DoesNotExist:
        log.warning("tenantchats does not exist: %s", tenant_chats_id)
    except TenantChats.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple tenantchats found for tenantchats ID: %s", tenant_chats_id)
    except Exception:
        log.exception("tenantchats lookup error for tenantchats ID: %s", tenant_chats_id)
    
    return tenantchats



### Save methods
def save_tenant_chat(**kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    tenant_chats_id (None if fail)
    created
    """
    # if not tenant_chats_id:
    #     return None, False
    
    tenantchats = None
    try:
        tenant_id = kwargs.get('tenant_id')
        chat_id = kwargs.get('chat_id')
        tenantchats, created = TenantChats.objects.get_or_create(
            # tenant_chats_id=tenant_chats_id,
            tenant_id=tenant_id,
            chat_id=chat_id

        )

        

        tenantchats.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "tenant chats id save error: (tenant chats id: %s, tenant id: %s, chat id: %s)",
            tenant_id, tenant_id, chat_id
        )
        return None, False
    
    return tenantchats, created