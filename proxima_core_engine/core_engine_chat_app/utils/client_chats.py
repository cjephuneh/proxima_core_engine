import logging

from django.db import DatabaseError, IntegrityError

from core_engine_chat_app.models import ClientChats
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_client_chat_from_id(client_chats_id):
    clientchats = None
    try:
        clientchats = ClientChats.objects.get(client_chats_id=client_chats_id)
    except ClientChats.DoesNotExist:
        log.warning("ClientChats does not exist: %s", client_chats_id)
    except ClientChats.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple ClientChatss found for ClientChats ID: %s", client_chats_id)
    except Exception:
        log.exception("ClientChats lookup error for ClientChats ID: %s", client_chats_id)
    
    return clientchats



### Save methods
def save_client_chats( **kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    clientchats (None if fail)
    created
    """
    # if not client_chats_id:
    #     return None, False
    
    clientchats = None
    try:
        client_id = kwargs.get('client_id')
        chat_id = kwargs.get('chat_id')

        clientchats, created = ClientChats.objects.get_or_create(
            # client_chats_id=client_chats_id,
            client_id=client_id,
            chat_id=chat_id,

        )
        
        clientchats.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Client chat save error: (client chats id: %s,  client id: %s, chat id: %s)",
            client_id, client_id, chat_id
        )
        return None, False
    
    return clientchats, created