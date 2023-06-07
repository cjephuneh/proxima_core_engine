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
    Create or update chat instance
    
    Return:
    chat (None if fail)
    created
    """
    chat = None
    try:
        tenant_id = kwargs.get('tenant_id')
        guest_client_id = kwargs.get('guest_client')
        chat_owner_id = kwargs.get('chat_owner')
        client_satisfaction = kwargs.get('client_satisfaction')
        
        try:
            tenant = Tenant.objects.get(tenant_id=tenant_id)
        except Tenant.DoesNotExist:
            log.error("Invalid tenant_id: %s", tenant_id)
            return None, False
        
        try:
            guest_client = Client.objects.get(id=guest_client_id)
        except Client.DoesNotExist:
            log.error("Invalid guest_client id: %s", guest_client_id)
            return None, False
        
        try:
            chat_owner = Client.objects.get(id=chat_owner_id)
        except Client.DoesNotExist:
            log.error("Invalid chat_owner id: %s", chat_owner_id)
            return None, False
        
        chat, created = Chat.objects.get_or_create(
            tenant_id=tenant,
            guest_client=guest_client,
            chat_owner=chat_owner,
            client_satisfaction=client_satisfaction
        )
        
        chat.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Chat save error: (Chat tenant: %s, Chat guest_client: %s, Chat chat_owner: %s)",
            tenant_id, guest_client_id, chat_owner_id
        )
        return None, False
    
    return chat, created
