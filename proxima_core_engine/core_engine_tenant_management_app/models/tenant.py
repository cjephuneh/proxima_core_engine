import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Tenant(MetaDataBase):
    tenant_id = models.AutoField(primary_key=True,
                                  help_text="The tenant chats ID.")

    tenant_name = models.CharField(max_length=30,
                            help_text="name of the company")
    industry = models.CharField(max_length=30,
                            help_text="industry of the company")
    

    def __int__(self):
        return str(self.tenant_id)

