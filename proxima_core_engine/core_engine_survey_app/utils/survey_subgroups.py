import logging

from django.db import DatabaseError, IntegrityError

from core_engine_survey_app.models import (
     SurveySubGroups, Survey 
     )
log = logging.getLogger(__name__)


### Retrieval methods
def get_surveysubgroup_from_id(survey_subgroups_id):
    surveysubgroups = None
    try:
        survey_subgroups_id = SurveySubGroups.objects.get(survey_subgroups_id=survey_subgroups_id)
    except surveysubgroups.DoesNotExist:
        log.warning("survey subgroup does not exist: %s", survey_subgroups_id)
    except SurveySubGroups.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple surveys found for survey_subgroups_ids ID: %s", survey_subgroups_id)
    except Exception:
        log.exception("survey lookup error for survey ID: %s", survey_subgroups_id)
    return surveysubgroups


### Save methods
def save_survey_subgroup(**kwargs):
    """
    Create or update survey  instance
    
    Return:
    surveysubgroups response (None if fail)
    created
    """
    
    surveysubgroups = None
    try:
        
        survey_id = kwargs.get('survey_id')
        subgroup_name = kwargs.get('subgroup_name')
        subgroup_description = kwargs.get('subgroup_description')
        # subgroup_clients = kwargs.get('subgroup_clients')

        surveysubgroups, created = SurveySubGroups.objects.get_or_create(
            survey_id = Survey.objects.get(survey_id=survey_id),
            subgroup_name=subgroup_name,
            subgroup_description=subgroup_description,
            # subgroup_clients=subgroup_clients
        )
        
        surveysubgroups.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Survey  subgroup save error: (survey_id ID: %s, subgroup_name : %s,  subgroup_description %s)",
            survey_id, subgroup_name, subgroup_description
        )
        return None, False
    
    return surveysubgroups, created