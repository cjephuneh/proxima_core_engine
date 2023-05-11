import uuid
from django.db import models

# Create your models here.
class AnonymousUser(models.Model):

    """
    Stores information about anonymous user
    """
    anonymous_user_id = models.AutoField(primary_key=True,
                            help_text="The webhookevent chats ID UUID.")
    contact = models.CharField(max_length=255,
                            help_text="Contact related to an anonymous user")
    name = models.CharField(max_length=200,
                                   help_text="")
    authorsbio = models.TextField(max_length=255,
                            help_text="")
    summary = models.CharField(max_length=200,
                            help_text="")
    def __str__(self):
        return self.contact
 