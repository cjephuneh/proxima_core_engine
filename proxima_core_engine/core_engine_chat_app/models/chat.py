import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Chat(MetaDataBase):
    """
    Stores information about a chat - beetween a client and tenant
    A tenant can have multiple chats with different client
    A client also can have multiple chats with different tenant
    A chat is a conversation beetween a client and a tenant
    a tenant can have many chats - i.e with many users
    A user can have only one chat with a single tenant. 
    A  chat has many messages beetween it
    The procedure is that first a chat beetween a client and a tenant is created 

    From there messages are added to that chat and when displayinhg the data then first the
    chat is pulled and messages endpoint hit to get all the messages for that chat
    """    
    chat_id = models.AutoField(primary_key=True,
                                help_text="The chat ID UUID for an instance of a chat.")
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                help_text="Display name of the tenant")
    guest_client = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.CASCADE,
                                     related_name='guest_client', help_text="Invited participant in the chat", null=True, blank=True)
    chat_owner = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.CASCADE,
                                related_name='chat_owner', help_text="Display name of the client")
    client_satisfaction = models.BooleanField(default=False, null=True,
                                              help_text="Whether client is satisfied or not")
    # A tenant will be able to set whether a client should have virtual assistant enabled 
    # if their package has that 
    # If they don't have the virtual agent enabled then all their chats will by default
    # have this disabled then when they switch all chats should default back to true
    iva_enabled = models.BooleanField(default=True, 
                                      help_text="Enable or disable whether the virtual assistant should talk to a client")


    def __str__(self):
        return str(self.chat_id)