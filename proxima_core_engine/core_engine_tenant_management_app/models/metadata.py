import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase


class Metadata(MetaDataBase):
    metadata_id = models.AutoField(primary_key=True,
                                  help_text="The tenant chats ID UUID for all chats.")
    # tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
    #                             help_text="Display name of the tenant")
    tenant_id = models.JSONField(
                                help_text="Display name of the tenant")

    def __str__(self):
        return str(self.metadata_id)


