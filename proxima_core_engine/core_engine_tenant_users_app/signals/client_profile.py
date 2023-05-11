from django.db.models.signals import post_save
from django.dispatch import receiver

from core_engine_tenant_users_app.models import Client
from core_engine_users_profile_app.models import ClientProfile

@receiver(post_save, sender=Client)
def create_related_client_profile(sender, instance, created, *args, **kwargs):
    #We are doing this only once when user is created
    if instance and created:
        instance.clientprofile = ClientProfile.objects.create(client=instance)

