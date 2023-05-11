import logging

from django.db import DatabaseError, IntegrityError

from core_engine_survey_app.models import Survey
from core_engine_tenant_management_app.models import Tenant
from core_engine_tenant_users_app.models import Client
log = logging.getLogger(__name__)


### Retrieval methods
def get_survey_from_id(survey_id):
    survey = None
    try:
        survey_id = Survey.objects.get(survey_id=survey_id)
    except survey.DoesNotExist:
        log.warning("survey does not exist: %s", survey_id)
    except Survey.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple surveys found for survey_ids ID: %s", survey_id)
    except Exception:
        log.exception("survey lookup error for survey ID: %s", survey_id)
    return survey


### Save methods
def save_tenant_survey(**kwargs):
    """
    Create or update survey  instance
    
    Return:
    Survey response (None if fail)
    created
    """
    # if not chat_id:
    #     return None, False
    
    survey = None
    try:
        
        tenant_id = kwargs.get('tenant_id')
        survey_topic = kwargs.get('survey_topic')
        survey_description = kwargs.get('survey_description')
        survey_context = kwargs.get('survey_context')
        survey_questions = kwargs.get('survey_questions')
        survey_type = kwargs.get('survey_type')
        start_day = kwargs.get('start_day')
        end_day = kwargs.get('end_day')

        survey, created = Survey.objects.get_or_create(
            tenant_id = Tenant.objects.get(tenant_id=tenant_id),
            survey_topic=survey_topic,
            survey_description=survey_description,
            survey_context=survey_context,
            start_day=start_day,
            survey_type=survey_type,
            end_day=end_day,
            # target_audience=Client.objects.filter(id_in=target_audience),
        )
        
        survey.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Survey save error: (survey_id ID: %s, survey_topic : %s,  survey_description %s)",
            tenant_id, survey_topic, survey_description
        )
        return None, False
    
    return survey, created