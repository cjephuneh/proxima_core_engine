from django.db.models.signals import post_save
from django.dispatch import receiver

from core_engine_tenant_users_app.models import Admin
from core_engine_users_profile_app.models import AdminProfile

@receiver(post_save, sender=Admin)
def create_related_admin_profile(sender, instance, created, *args, **kwargs):
    #We are doing this only once when user is created
    if instance and created:
        instance.adminprofile = AdminProfile.objects.create(admin=instance)
