from django.contrib import admin

from core_engine_tenant_management_app.models import (
    address, metadata ,products , tenant  
)

@admin.register(tenant.Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('tenant_id', 'tenant_name', 'industry')
    # raw_id_fields = ('tenant_id', )
    # autocomplete_fields = ('skills',)

    search_fields = ('tenant_id',)

@admin.register(products.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'tenant_id', 'name', 'description', 'price')
    raw_id_fields = ('tenant_id',)

    search_fields = ('product_id', )


@admin.register(address.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'city', 'country', 'postal_code', 'state', 'payment_number')
    raw_id_fields = ('tenant_id',)

    search_fields = ('address_id', )


@admin.register(metadata.Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = ('metadata_id', 'tenant_id')
    # raw_id_fields = ('tenant_id',)

    search_fields = ('metadata_id', )


