import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class SurveyReport(MetaDataBase):
    survey_report_id = models.AutoField(primary_key=True,
                                help_text="The survey report id")
    survey_id = models.ForeignKey("core_engine_survey_app.Survey", on_delete=models.CASCADE,
                                  help_text="Display name of the survey")
    conclusion =models.TextField( 
                                     help_text="The survey subgroup name")
    survey_success = models.BooleanField(default=False,
                                         help_text="The survey success")
    survey_reporter = models.ForeignKey("core_engine_tenant_users_app.Employee", on_delete=models.CASCADE,
                                        help_text="Employee who made the survey review")

    def __str__(self):
        return str(self.survey_report_id)



