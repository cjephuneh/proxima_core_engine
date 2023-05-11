from django.db import models

# Create your models here.
from django.db import models
from core_engine_tenant_users_app.models import User
# from core_engine_tenant_users_app.models import ClientManager
from django.contrib.auth.models import (
    PermissionsMixin
)

from django.contrib.auth.models import (
    BaseUserManager
)
# Create your models here.

"""
The Client User Manager
"""
class ClientManager(BaseUserManager):
    def create_client(self, username, first_name, last_name, phonenumber, email, gender,DOB,user_type, password=None, confirm_password=None):
        if email is None:
            raise TypeError("Users must have a email address")

        if not password or not confirm_password:
            raise TypeError("Please enter a password and "
                "confirm it.")

        if password != confirm_password:
            raise TypeError("Those passwords don't match.")
            
        client = Client(username=username,first_name=first_name, last_name=last_name, phonenumber=phonenumber, email=self.normalize_email(email),
                        gender=gender, DOB=DOB,user_type=user_type)

        client.set_password(password)
        client.save()
        return client
    
class Client(User, PermissionsMixin):
    """
    Stores information about a client
    """

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB', 'user_type' ]

    objects = ClientManager()

    def __str__(self):
        return str(self.username)  