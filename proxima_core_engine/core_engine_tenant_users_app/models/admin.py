from django.db import models

# Create your models here.
from django.db import models
from core_engine_tenant_users_app.models import User
# from core_engine_tenant_users_app.models import AdminManager
from django.contrib.auth.models import (
    BaseUserManager
)
from django.contrib.auth.models import (
 PermissionsMixin
)

class AdminManager(BaseUserManager):
    def create_admin(self, username, first_name, last_name, phonenumber, email, gender,tenant_id,DOB,user_type, password=None, confirm_password=None):
        if email is None:
            raise TypeError("Users must have a email address")

        if not password or not confirm_password:
            raise TypeError("Please enter a password and "
                "confirm it.")

        if password != confirm_password:
            raise TypeError("Those passwords don't match.")
            
        admin = Admin(username=username, first_name=first_name, last_name=last_name, phonenumber=phonenumber, email=self.normalize_email(email),
                        gender=gender,tenant_id=tenant_id, DOB=DOB,user_type=user_type)

        admin.set_password(password)
        admin.save()
        return admin
    
class Admin(User, PermissionsMixin):
    """
    Stores information on Admin users
    """
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                help_text="Display id of the tenant")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB', 'user_type','tenant_id' ]

    objects = AdminManager()

    def __str__(self):
        return str(self.username) 
 
