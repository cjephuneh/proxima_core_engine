import logging

from django.db import DatabaseError, IntegrityError

from core_engine_chat_app.models import Chat
from core_engine_tenant_users_app.models import Client
from core_engine_community_app.models import Thread
from core_engine_chat_app.models import Message
# save_anonymous_user

log = logging.getLogger(__name__)


def call_tenant_virtual_assistant_endpoint(tenant_id, message):
    pass

def save_message_model_instance(**kwargs):
        
    message = None
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

    return message, created

def virtual_assistant_handler(**kwargs):
    """
    Talk to a virtual assistant

    Return:
    - Virtual Assistant Response (None if fail)
    - sent
    """

    tenant_id = kwargs.get('tenant_id')
    message = kwargs.get('message')

    try:
        # Save the client message to the database
        save_message_model_instance(**kwargs)

        # Call the tenant virtual assistant endpoint
        virtual_assistant_response = call_tenant_virtual_assistant_endpoint(tenant_id, message)

        # Update kwargs with virtual assistant response
        kwargs.update(
            message=virtual_assistant_response,
            message_sender='tenant_iva'
        )

        # Save the virtual assistant response to the database
        save_message_model_instance(**kwargs)

        return virtual_assistant_response, True

    except (IntegrityError, DatabaseError) as e:
        log.error("Error saving message: %s", str(e))
        return None, False
