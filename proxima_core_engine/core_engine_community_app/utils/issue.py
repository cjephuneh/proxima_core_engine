import logging

from django.db import DatabaseError, IntegrityError

from core_engine_community_app.models import Issue
from core_engine_tenant_users_app.models import Client
from core_engine_community_app.models import Community
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_community_issue_id(issue_id):
    issue = None
    try:
        issue = Issue.objects.get(issue_id=issue_id)
    except Issue.DoesNotExist:
        log.warning("issue does not exist: %s", issue_id)
    except Issue.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple issues found for issue ID: %s", issue_id)
    except Exception:
        log.exception("issue lookup error for issue ID: %s", issue_id)
    
    return issue



### Save methods
def save_community_issue(**kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    issue (None if fail)
    created
    """
    # if not issue_id:
    #     return None, False
    
    issue = None
    try:

        client_id = kwargs.get('client_id')
        issue = kwargs.get('issue')
        community_id = kwargs.get('community_id')
        description = kwargs.get('description')
        solved = kwargs.get('solved')

        issue, created = Issue.objects.get_or_create(
            # issue_id=issue_id,
            client_id=Client.objects.get(id=client_id),
            issue=issue,
            community_id=Community.objects.get(community_id=community_id),
            description=description,
            solved=solved,

        )
        
        issue.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Issue save error: (Anonymous user ID: %s, client_id: %s, issue: %s)",
            client_id, client_id, issue
        )
        return None, False
    
    return issue, created