import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Response(MetaDataBase):
    response_id = models.AutoField(primary_key=True,
                                help_text="The lilling details id ID UUID")
    survey_id = models.ForeignKey("core_engine_survey_app.Survey", on_delete=models.CASCADE,
                                help_text="Display name of the tenant")
    client = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.DO_NOTHING,
                                help_text="")
    survey_response = models.JSONField(null=True, blank=True,
                                        help_text="The survey response")

    def __str__(self):
        return str(self.response_id)


