import logging

from django.db import DatabaseError, IntegrityError

from core_engine_tenant_users_app.models import AnonymousUser
# save_anonymous_user

log = logging.getLogger(__name__)


### Retrieval methods
def get_anonymous_user_from_id(anonymous_user_id):
    anonymoususer = None
    try:
        anonymoususer = AnonymousUser.objects.get(anonymous_user_id=anonymous_user_id)
    except AnonymousUser.DoesNotExist:
        log.warning("AnonymousUser does not exist: %s", anonymous_user_id)
    except AnonymousUser.MultipleObjectsReturned:
        # Shouldn't happen
        log.error("Multiple AnonymousUsers found for AnonymousUser ID: %s", anonymous_user_id)
    except Exception:
        log.exception("AnonymousUser lookup error for AnonymousUser ID: %s", anonymous_user_id)
    
    return anonymoususer



### Save methods
def save_anonymous_user(anonymous_user_id, org=None, **kwargs):
    """
    Create or update anonymous user instance
    
    Return:
    anonymoususer (None if fail)
    created
    """
    if not anonymous_user_id:
        return None, False
    
    anonymoususer = None
    try:
        anonymoususer, created = AnonymousUser.objects.get_or_create(
            anonymous_user_id=anonymous_user_id,
            # defaults={
            #     'platform': get_default_platform()
            # }
        )
        # Retrieve platform from org if it exists, otherwise don't change
        # if anonymoususer:
        #     anonymoususer = get_platform_from_org(org)
        # if platform:
        #     tenant.platform = platform
        
        tenant_name = kwargs.get('tenant_name')
        if tenant_name is not None:
            tenant.tenant_name = tenant_name
        
        anonymoususer.save()
    except (IntegrityError, DatabaseError):
        log.error(
            "Anonymous user save error: (Anonymous user ID: %s, Anonymous user_name: %s, Platform: %s)",
            anonymous_user_id, tenant_name
        )
        return None, False
    
    return anonymoususer, created