# from django.db.models.signals import post_save
# from django.dispatch import receiver


# from core_engine_tenant_management_app.models import Tenant
# from core_engine_community_app.models import Community

# """
# Whenever an instance of a tenant is created  - a subsequent community should also be created
# """
# @receiver(post_save, sender=Tenant)
# def create_related_entities(sender, instance, created, *args, **kwargs):
#     #We are doing this only once when user is created
#     if instance and created:
#         instance.community = Community.objects.create(tenant=instance)

