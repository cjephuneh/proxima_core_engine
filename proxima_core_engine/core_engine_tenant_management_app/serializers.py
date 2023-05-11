from rest_framework import serializers

from core_engine_tenant_management_app.models import (
    address, metadata ,products , tenant  
)


# Tenant serializers

class TenantSerializer(serializers.ModelSerializer):
    tenant_id = serializers.CharField(
        source='core_engine_tenant_management_app.tenant', default=None
    )
    class Meta:
        model = tenant.Tenant
        fields = ('tenant_id', 'tenant_name', 'industry')
        # read_only_fields = fields


# Product serializers

class ProductSerializer(serializers.ModelSerializer):
    tenant_id = serializers.CharField(
        source='core_engine_tenant_management_app.tenant', default=None
    )
    class Meta:
        model = products.Product
        fields = ('product_id', 'tenant_id', 'name', 'description', 'price')
        # read_only_fields = ('position',)


# Address serializers

class AddressSerializer(serializers.ModelSerializer):

    community_id = serializers.CharField(
        source='core_engine_community_app.Community', default=None
    )
    class Meta:
        model = address.Address
        fields = ('address_id', 'city', 'country', 'community_id', 'postal_code', 'state', 'payment_number')
        # read_only_fields = ('position',)


class MetadataSerializer(serializers.ModelSerializer):
    tenant_id = serializers.CharField(
        source='core_engine_tenant_management_app.tenant', default=None
    )
    class Meta:
        model = metadata.Metadata
        fields = ('metadata_id', 'tenant_id')
        # read_only_fields = fields


