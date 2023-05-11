import logging

from django.db import DatabaseError, IntegrityError

from core_engine_chat_app.models import Message
from core_engine_chat_app.models import Chat
# save_anonymous_user

log = logging.getLogger(__name__)


### Retrieval methods
def get_message_from_id(message_id):
    message = None
    try:
        message = Message.objects.get(message_id=message_id)
    except Message.DoesNotExist:
        log.warning("Message does not exist: %s", message_id)
    except Message.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple Messages found for Message ID: %s", message_id)
    except Exception:
        log.exception("Message lookup error for Message ID: %s", message_id)
    
    return message



### Save methods
def save_chat_message( **kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    Message (None if fail)
    created
    """
    # if not message_id:
    #     return None, False
    
    message = None
    try:
        chat_id = kwargs.get('chat_id')
        text_content = kwargs.get('text_content')
        voice_content = kwargs.get('voice_content')
        sent_at = kwargs.get('sent_at')
        message_sender = kwargs.get('message_sender')
        escalated = kwargs.get('escalated')
        channel = kwargs.get('channel')
        topic = kwargs.get('topic')
        message, created = Message.objects.get_or_create(
            chat_id=Chat.objects.get(chat_id=chat_id),
            text_content=text_content,
            voice_content=voice_content,
            sent_at=sent_at,
            message_sender=message_sender,
            escalated=escalated,
            channel=channel,
            topic=topic

        )
        

        message.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Message save error: (message id: %s, chat id: %s, text content: %s)",
            chat_id, chat_id, text_content
        )
        return None, False
    
    return message, created