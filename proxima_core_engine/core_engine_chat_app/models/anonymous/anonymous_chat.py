import uuid
from django.db import models

class AnonymousChat(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anonymous_user_id = models.ForeignKey(max_length=1000)
    tenant_id = models.ForeignKey()



"""
A chat is a conversation beetween a client and a tenant
a tenant can have many chats - i.e with many users
A user can have only one chat with a single tenant. 
A  chat has many messages beetween it
"""

"""
The procedure is that first a chat beetween a client and a tenant is created 
"""

"""
From there messages are added to that chat and when displayinhg the data then first the
chat is pulled and messages endpoint hit to get all the messages for that chat
"""