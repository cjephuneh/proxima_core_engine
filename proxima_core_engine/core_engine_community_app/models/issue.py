import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

# Settimg up the chat body template

class Issue(MetaDataBase):
    """
    Stores information about a topic created by a tenant 
    """
    issue_id = models.AutoField(primary_key=True,
                                help_text="The issue ID UUID .")
    # Cliet that created the issue
    client_id = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.CASCADE,
                                help_text="Display name of the client")
    issue = models.CharField(max_length=100,
                                help_text="Display name of the issue that's created")
    community_id = models.ForeignKey("core_engine_community_app.Community", on_delete=models.CASCADE,
                                help_text="Display name of the community")
    description = models.TextField(max_length=255, 
                                help_text="Description of the issue")
    solved = models.BooleanField(default=False,
                                help_text="Was the issue solved or not")


    def __str__(self):
        return str(self.issue_id)