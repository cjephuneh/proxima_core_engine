# import pytest

# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient

# from core_engine_tenant_management_app.models import Tenant, Product, Metadata
# from core_engine_tenant_management_app.serializers import (
#     TenantSerializer,
#     ProductSerializer,
#     MetadataSerializer,
# )
# from core_engine_tenant_management_app.utils import save_tenant, save_tenant_product, save_tenant_metadata


# @pytest.fixture
# def tenant_data():
#     return {"tenant_id": 1, "tenant_name": "Test Tenant"}


# @pytest.fixture
# def product_data():
#     return {
#         "product_id": "test_product",
#         "tenant_id": 1,
#         "name": "Test Product",
#         "description": "Test Product Description",
#         "price": "10.99",
#     }


# @pytest.fixture
# def metadata_data():
#     return {
#         "metadata_id": "test_metadata",
#         "tenant_id": "test_tenant",
#         "key": "Test Metadata",
#         "value": "Test Metadata Value",
#     }


# @pytest.mark.django_db
# class TestTenantView:
#     def test_get_tenant(self, tenant_data):
#         tenant, created = save_tenant(**tenant_data)
#         client = APIClient()
#         url = reverse("tenant_urls:core_tenant")
#         response = client.get(url, {"tenant_id": tenant.tenant_id})
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == TenantSerializer(tenant).data

#     def test_post_tenant(self, tenant_data):
#         client = APIClient()
#         url = reverse("tenant_urls:core_tenant")
#         response = client.post(url, tenant_data, format="json")
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data == TenantSerializer(Tenant.objects.first()).data

#     def test_delete_tenant(self, tenant_data):
#         tenant, created = save_tenant(**tenant_data)
#         client = APIClient()
#         url = reverse("tenant_urls:core_tenant")
#         response = client.delete(url, {"tenant_id": tenant.tenant_id})
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {"count": 1, "type": "core_engine_tenant_management_app.Tenant"}

#     def test_delete_tenant_invalid(self):
#         client = APIClient()
#         url = reverse("tenant_urls:core_tenant")
#         response = client.delete(url, {"tenant_id": "non_existent_tenant"})
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {"count": 0, "type": "core_engine_tenant_management_app.Tenant"}


# @pytest.mark.django_db
# class TestProductView:
#     def test_get_product(self, product_data):
#         product, created = save_tenant_product(**product_data)
#         client = APIClient()
#         url = reverse("tenant_urls:core_tenant_product")
#         response = client.get(url, {"product_id": product.product_id})
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == ProductSerializer(product).data

#     def test_post_product(self, product_data):
#         client = APIClient()
#         url = reverse("tenant_urls:core_tenant_product")
#         response = client.post(url, product_data, format="json")
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data == ProductSerializer(Product.objects.first()).data

#     def test_delete_product(self, product_data):
#         product, created = save_tenant_product(**product_data)
#         client = APIClient()
#         url = reverse("tenant_urls;core_tenant_product")
#         response = client.delete(url, {"product_id": product.product_id})
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {"count": 0, "type": "core_engine_tenant_management_app.Product"}
