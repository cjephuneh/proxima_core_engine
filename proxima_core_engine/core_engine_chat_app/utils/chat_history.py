# Utilities function that will get the chat history of a client

from core_engine_chat_app.models import Chat, Message

def get_client_chat_history(client_id, chat_id):

    """
    Filter params
    1. chat_id
    2. message_sender = client
    """

    chat_history = Message.objects.get(chat_id=chat_id)

    return chat_history