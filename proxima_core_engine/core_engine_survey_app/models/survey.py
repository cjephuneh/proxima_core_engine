import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Survey(MetaDataBase):

    SURVEY_TYPE = (
        ('open_ended', 'open_ended'), ('close_ended', 'close_ended')

    )
    survey_id = models.AutoField(primary_key=True,
                                help_text="The lilling details id ID UUID")
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                help_text="Display name of the tenant")
    survey_topic = models.CharField(max_length=255,
                                    help_text="The survey topic")
    survey_description = models.CharField(max_length=20,
                                          help_text="The survey description")
    survey_context = models.CharField(max_length=20,
                                      help_text="The survey context")
    survey_questions = models.JSONField(null=True, blank=True,
                                        help_text="The survey questions")
    target_audience = models.ManyToManyField("core_engine_tenant_users_app.Client", blank=True,
                                             help_text="The target audience/who to share with")
    survey_type = models.CharField(max_length=20, choices=SURVEY_TYPE, null=True, blank=True,
                                   help_text="The survey type")
    start_day = models.DateField(null=True, blank=True,
                                 help_text="The start day of the survey")
    end_day = models.DateField(null=True, blank=True,
                               help_text="The end day of the survey") 


    def __str__(self):
        return str(self.survey_id)



