from django.db.models.signals import post_save
from django.dispatch import receiver
from core_engine_tenant_management_app.models import Tenant
from core_engine_community_app.models import Community

@receiver(post_save, sender=Tenant)
def create_community(sender, instance, created, **kwargs):
    if created:
        community = Community.objects.create(
            community_name=f"{instance.tenant_name} Community",
            tenant_id=instance,
            description=f"Community for {instance.tenant_name}",
        )
