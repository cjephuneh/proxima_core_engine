import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Product(MetaDataBase):
    product_id = models.AutoField(primary_key=True,
                                  help_text="The tenant chats ID UUID for all chats.")
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                help_text="Display name of the tenant")
    name = models.CharField(max_length=30,
                            help_text="name of the product")
    description = models.TextField(max_length=200,
                                   help_text="description of the product")
    price = models.CharField(max_length=30,
                            help_text="price of the product")

    def __str__(self):
        return str(self.product_id)
    
