from django.db import models
from core_engine_utils_app.models import MetaDataBase
# Create your models here.

class EmployeeProfile(MetaDataBase):
    employee = models.OneToOneField("core_engine_tenant_users_app.Employee", on_delete=models.CASCADE,
                                help_text="Display name of the employee")
    profile_photo  = models.ImageField()
    country = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    """
    A suggestion to pick from using Google Maps API 
    """

    def __str__(self):
        return str(self.employee)

    
