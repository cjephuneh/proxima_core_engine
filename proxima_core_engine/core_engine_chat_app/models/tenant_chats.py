import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class TenantChats(MetaDataBase):
    """
    Stores all messages beetween a tenant and the clients who communicate with it
    """
    tenant_chats_id = models.AutoField(primary_key=True,
                                  help_text="The tenant chats ID UUID for all chats.")
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                help_text="Display name of the tenant")
    chat_id = models.ForeignKey("core_engine_chat_app.Chat", on_delete=models.CASCADE,
                                help_text="Display name of the chat")
    
    def __str__(self):
        return self.tenant_chats_id