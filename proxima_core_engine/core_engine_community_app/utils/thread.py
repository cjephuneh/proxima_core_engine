import logging

from django.db import DatabaseError, IntegrityError

from core_engine_community_app.models import Thread, Issue

log = logging.getLogger(__name__)



### Retrieval methods
def get_issue_from_id(thread_id):
    thread = None
    try:
        thread = Thread.objects.get(thread_id=thread_id)
    except Thread.DoesNotExist:
        log.warning("thread does not exist: %s", thread_id)
    except Thread.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple threads found for thread ID: %s", thread_id)
    except Exception:
        log.exception("thread lookup error for thread ID: %s", thread_id)
    
    return thread



### Save methods
def save_issue_thread( **kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    thread (None if fail)
    created
    """
    # if not thread_id:
    #     return None, False
    
    thread = None
    try:
        issue_id = kwargs.get('issue_id')
        thread, created = Thread.objects.get_or_create(
            # thread_id=thread_id,
            issue=Issue.objects.get(issue_id=issue_id),

        )
        
        
        thread.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Thread save error: (thread_id: %s, issue: %s)",
            issue_id, issue_id
        )
        return None, False
    
    return thread, created