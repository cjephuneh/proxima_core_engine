import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Message(MetaDataBase):
    """
    Stores information about a message
    In the db content and voice note can be null but from ui form will not be
    sublitted if values are null
    """

    SENDER = (
        ('client', 'client'), ('tenant','tenant'), ('tenant_iva', 'tenant_iva')

    )

    CHANNELS = (
        ('Mobile', 'Mobile'),
        ('Website', 'Website'),

    )
    message_id = models.AutoField(primary_key=True,
                                  help_text="The message ID UUID for an instance of a chat.")
    chat_id = models.ForeignKey("core_engine_chat_app.Chat", on_delete=models.CASCADE,
                                help_text="The chat ID UUID for an instance of a chat.")
    text_content = models.CharField(max_length=255,null=True,blank=True,
                                    help_text="Message text content")
    voice_content = models.FileField(upload_to="media/voice_content",null=True,blank=True,
                                     help_text="The voice note sent")
    sent_at = models.DateTimeField(auto_now_add=True,
                                   help_text="Time that the message has been sent")
    message_sender = models.CharField(choices=SENDER ,max_length=50,
                                      help_text="Either the message is sent by the agent or by the tenant")
    escalated = models.BooleanField(default=False, null=True, blank=True,
                                    help_text="Say whether a client escalated a chat to a human agent.")
    channel = models.CharField(choices=CHANNELS, max_length=200, null=True,
                               help_text='Channel from which message was sent')
    topic = models.CharField(choices=CHANNELS, max_length=200, null=True,
                               help_text='Message topic')


    def __str__(self):
        return str(self.message_id)