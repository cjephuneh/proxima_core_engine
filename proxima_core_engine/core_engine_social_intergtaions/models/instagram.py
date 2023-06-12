import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

# Settimg up the chat body template

class InstagramIntergration(MetaDataBase):
    """
    Stores information about instagram tenant intergrations
    """
    instagram_intergration_id = models.AutoField(primary_key=True,
                                help_text="The instagram social intergrations")
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                   help_text="Display name of the tenant.")  
    issue = models.CharField(max_length=100,
                                help_text="")
    description = models.TextField(max_length=255, 
                                help_text="")


    def __str__(self):
        return str(self.instagram_intergration_id)