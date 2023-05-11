import logging

from django.db import DatabaseError, IntegrityError

from core_engine_community_app.models import Comment
from core_engine_tenant_users_app.models import Client
from core_engine_community_app.models import Thread
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_client_comment_from_id(comment_id):
    comment = None
    try:
        comment = Comment.objects.get(comment_id=comment_id)
    except Comment.DoesNotExist:
        log.warning("comment does not exist: %s", comment_id)
    except Comment.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple comments found for comment ID: %s", comment_id)
    except Exception:
        log.exception("comment lookup error for comment ID: %s", comment_id)
    
    return comment



### Save methods
def save_client_comment(**kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    comment (None if fail)
    created
    """
    # if not comment_id:
    #     return None, False
    
    comment = None
    try:
        thread = kwargs.get('thread')
        client = kwargs.get('client')
        # issue = kwargs.get('issue')
        comment_description = kwargs.get('comment_description')
        likes = kwargs.get('likes')
        dislikes = kwargs.get('dislikes')

        comment, created = Comment.objects.get_or_create(
            # comment_id=comment_id,
            thread=Thread.objects.get(thread_id=thread),
            client=Client.objects.get(id=client),
            comment_description=comment_description,
            # likes=likes,
            # dislikes=dislikes,

        )
        
        comment.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Comment save error: (comment_id: %s, thread: %s, client: %s)",
            thread,thread, client
        )
        return None, False
    
    return comment, created