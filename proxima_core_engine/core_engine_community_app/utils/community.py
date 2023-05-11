import logging

from django.db import DatabaseError, IntegrityError

from core_engine_community_app.models import Community
# save_anonymous_user

log = logging.getLogger(__name__)



### Retrieval methods
def get_tenant_community_from_id(community_id):
    community = None
    try:
        community = Community.objects.get(community_id=community_id)
    except Community.DoesNotExist:
        log.warning("community does not exist: %s", community_id)
    except Community.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple communitys found for community ID: %s", community_id)
    except Exception:
        log.exception("community lookup error for community ID: %s", community_id)
    
    return community



### Save methods
def save_tenant_community(**kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    anonymoususer (None if fail)
    created
    """
    # if not community_id:
    #     return None, False
    
    community = None
    try:
        tenant_id = kwargs.get('tenant_id')
        description = kwargs.get('description')
        community, created = Community.objects.get_or_create(
            # community_id=community_id,
            tenant_id=tenant_id,
            description=description,

        )

        
        community.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Community user save error: (community_id: %s, tenant_id: %s)",
            tenant_id, tenant_id
        )
        return None, False
    
    return community, created