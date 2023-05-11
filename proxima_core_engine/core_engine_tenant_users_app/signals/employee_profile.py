from django.db.models.signals import post_save
from django.dispatch import receiver

from core_engine_tenant_users_app.models import Employee
from core_engine_users_profile_app.models import EmployeeProfile

@receiver(post_save, sender=Employee)
def create_related_employee_profile(sender, instance, created, *args, **kwargs):
    #We are doing this only once when user is created
    if instance and created:
        instance.employeeprofile = EmployeeProfile.objects.create(employee=instance)

