import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Comment(MetaDataBase):
    """
    Stores information on comments made by clients
    """
    comment_id = models.AutoField(primary_key=True,
                                    help_text="The chat ID UUID for an instance of a issue.")

    thread = models.ForeignKey("core_engine_community_app.Thread", on_delete=models.CASCADE,
                                help_text="Display name of the Thread")
    client = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.CASCADE,
                                help_text="Display name of the client")
    comment_description = models.TextField(blank=True, null=True,
                                            help_text="Description of the comment")
    likes = models.ManyToManyField("core_engine_tenant_users_app.Client", blank=True, related_name='comment_likes',
                                   help_text="Users who liked the comment")
    dislikes = models.ManyToManyField("core_engine_tenant_users_app.Client", blank=True, related_name='comment_dislikes',
                                      help_text="Users who liked the comment")



    def __str__(self):
        return str(self.comment_id)