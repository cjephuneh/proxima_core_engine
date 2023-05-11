import uuid
from django.db import models

# Settimg up the chat body template
"""
Table for all chats that belong to a tenant
Will be a signal that for each time a chat is created for a tenant then it's added to the TenantChats model
"""
class AnonymousTenantChats(models.Model):
    user_chats_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.ForeignKey()
    chat_id = models.ForeignKey()