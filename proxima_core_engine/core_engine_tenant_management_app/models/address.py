import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase

class Address(MetaDataBase):
    address_id = models.AutoField(primary_key=True,
                                  help_text="Address id of the tenant")
    tenant_id = models.OneToOneField("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                help_text="Display name of the tenant")
    billing_details_id = models.CharField(max_length=30,
                            help_text="Billing details of tyhe tenant")
    city = models.CharField(max_length=30,
                            help_text="City which the tenant comes from")
    country = models.CharField(max_length=30,
                            help_text="Country of yhe tenant")
    postal_code = models.CharField(max_length=30,
                            help_text="Postal code of the tenant")
    state = models.CharField(max_length=30,
                            help_text="Statement which the tenant comes from")
    payment_number = models.CharField(max_length=30,
                            help_text="If for mobile transaction - the phone number to use")


    def __str__(self):
        return str(self.address_id)

