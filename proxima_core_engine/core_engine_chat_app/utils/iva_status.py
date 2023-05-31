# This function will activate or disable the virtual assistant for
# for a chat

from core_engine_chat_app.models import Chat

def iva_status(client_id, chat_id, tenant_id):
    enable_iva = ""