import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class SurveySubGroups(MetaDataBase):
    survey_subgroups_id = models.AutoField(primary_key=True,
                                help_text="The survey report id")
    survey_id = models.ForeignKey("core_engine_survey_app.Survey", on_delete=models.CASCADE,
                                  help_text="Display name of the survey")
    subgroup_name = models.CharField(max_length=255, 
                                     help_text="The survey subgroup name")
    subgroup_description = models.CharField(max_length=255, 
                                     help_text="The survey subgroup description")
    subgroup_clients = models.ManyToManyField("core_engine_tenant_users_app.Client", blank=True,
                                              help_text="The subgroup clients")


    def __str__(self):
        return str(self.survey_subgroups_id)



