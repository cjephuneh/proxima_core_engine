import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase


class ClientChats(MetaDataBase):
    """
    Stores all chats that belong to a particular client
    Will be a signal that for each time a chat is created for a client then it's added to the TenantChats model
    """
    client_chats_id = models.AutoField(primary_key=True,
                                help_text="The chat ID UUID for an instance of a chat.")
    client_id = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.CASCADE,
                                help_text="Display name of the client")
    chat_id = models.ForeignKey("core_engine_chat_app.Chat", on_delete=models.CASCADE,
                                help_text="Display name of the chat")

    def __str__(self):
        return self.client_chats_id