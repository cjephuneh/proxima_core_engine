import logging

from django.db import DatabaseError, IntegrityError

from core_engine_chat_app.models import Chat
from core_engine_survey_app.models import Survey, Response
from core_engine_tenant_users_app.models import Client

log = logging.getLogger(__name__)


### Retrieval methods
def get_response_from_id(response_id):
    response = None
    try:
        response_id = Response.objects.get(response_id=response_id)
    except response.DoesNotExist:
        log.warning("response does not exist: %s", response_id)
    except Response.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple responses found for response_ids ID: %s", response_id)
    except Exception:
        log.exception("response lookup error for response ID: %s", response_id)
    return response


### Save methods
def save_client_survey_response(**kwargs):
    """
    Create or update chat  instance
    
    Return:
    Survey response (None if fail)
    created
    """
    # if not chat_id:
    #     return None, False
    
    response = None
    try:
        
        survey_id = kwargs.get('survey_id')
        client = kwargs.get('client')
        survey_response = kwargs.get('survey_response')

        response, created = Response.objects.get_or_create(
        # response = Response.objects.create(
            survey_id=Survey.objects.get(survey_id=survey_id),
            client=Client.objects.get(id=client),
            survey_response=survey_response
        )

        # created = True
        
        response.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Survey save error: (survey_id ID: %s, Client : %s,  response %s)",
            survey_id, client, survey_response
        )
        return None, False
    
    return response, created