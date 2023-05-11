import uuid
from django.db import models

# Settimg up the chat body template

class AnonymousMessage(models.Model):

    CHANNELS = (
        ('WhatsApp', 'WhatsApp'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('Website', 'Website'),
        ('Text', 'Text'),

    )
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anonymous_chat_id = models.ForeignKey()
    type = models.CharField()
    text_content = models.CharField(null=True)
    voice_content = models.FileField(null=True)
    sent_at = models.DateTimeField()
    delivered_at = models.DateTimeField()
    message_sender = models.CharField(max_length=50)
    chat_means = models.CharField(choices=CHANNELS, max_length=200)  # SOURCE
    user_query = models.CharField(max_length=1000)
    agent_response = models.CharField(max_length=1000)
    escalated = models.BooleanField(default=False)
    topic = models.CharField(max_length=1000, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)


"""
In the db content and voice note can be null but from ui form will not be
sublitted if values are null
"""