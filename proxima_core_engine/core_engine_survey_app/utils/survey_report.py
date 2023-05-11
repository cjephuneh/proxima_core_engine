import logging

from django.db import DatabaseError, IntegrityError

from core_engine_survey_app.models import (
     Survey, SurveyReport
     )
from core_engine_tenant_users_app.models import Employee
log = logging.getLogger(__name__)


### Retrieval methods
def get_surveyreport_from_id(survey_report_id):
    surveyreport = None
    try:
        survey_report_id = SurveyReport.objects.get(survey_report_id=survey_report_id)
    except surveyreport.DoesNotExist:
        log.warning("survey subgroup does not exist: %s", survey_report_id)
    except SurveyReport.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple surveys reports found for survey_report_ids ID: %s", survey_report_id)
    except Exception:
        log.exception("survey lookup error for survey ID: %s", survey_report_id)
    return surveyreport


### Save methods
def save_survey_report(**kwargs):
    """
    Create or update survey  instance
    
    Return:
    survey_report response (None if fail)
    created
    """
    
    surveyreport = None
    try:
        survey_id = kwargs.get('survey_id')
        conclusion = kwargs.get('conclusion')
        survey_success = kwargs.get('survey_success')
        survey_reporter = kwargs.get('survey_reporter')

        surveyreport, created = SurveyReport.objects.get_or_create(
            survey_id = Survey.objects.get(survey_id=survey_id),
            conclusion=conclusion,
            survey_success=survey_success,
            survey_reporter=Employee.objects.get(id=survey_reporter)
        )
        
        surveyreport.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Survey  subgroup save error: (survey_id ID: %s, conclusion : %s,  survey_reporter %s)",
            survey_id, conclusion, survey_reporter
        )
        return None, False
    
    return surveyreport, created