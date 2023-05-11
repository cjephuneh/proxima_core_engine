import logging

from django.db import DatabaseError, IntegrityError

from core_engine_chat_app.models import Chat
from core_engine_tenant_management_app.models import Tenant
from core_engine_tenant_users_app.models import Client
# save_anonymous_user

log = logging.getLogger(__name__)


### Retrieval methods
def get_chat_from_id(chat_id):
    chat = None
    try:
        chat_id = Chat.objects.get(chat_id=chat_id)
    except Chat.DoesNotExist:
        log.warning("Chat does not exist: %s", chat_id)
    except Chat.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple Chats found for chat_ids ID: %s", chat_id)
    except Exception:
        log.exception("Chat lookup error for Chat ID: %s", chat_id)
    return chat


### Save methods
def save_tenant_client_chat(**kwargs):
    """
    Create or update chat  instance
    
    Return:
    chat (None if fail)
    created
    """
    # if not chat_id:
    #     return None, False
    
    chat = None
    try:
        tenant = kwargs.get('tenant')
        guest_client = kwargs.get('guest_client')
        chat_owner = kwargs.get('chat_owner')
        client_satisfaction = kwargs.get('client_satisfaction')
        chat, created = Chat.objects.get_or_create(
            # chat_id=chat_id,
            tenant=Tenant.objects.get(tenant_id=tenant),
            guest_client=Client.objects.get(id=guest_client),
            chat_owner=Client.objects.get(id=chat_owner),
            client_satisfaction=client_satisfaction
        )
        
        chat.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Chat save error: (Chat ID: %s, Chat tenant: %s, Chat Client: %s)",
            chat_owner, tenant, chat_owner
        )
        return None, False
    
    return chat, created