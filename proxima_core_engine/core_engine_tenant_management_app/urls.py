from django.urls import include, path, re_path

from core_engine_tenant_management_app.views import (
    TenantView, ProductView, MetadataView, AddressView
)

app_name = 'core_engine_tenant_management_app'
urlpatterns = [
    re_path(r'^api/tenantmanagement/', include([
        # Signin
        re_path(r'^tenant/$', TenantView.as_view(), name='core_tenant'),
        re_path(r'^product/$', ProductView.as_view(), name='core_tenant_product'),
        re_path(r'^metadata/$', MetadataView.as_view(), name='core_tenant_metadata'),
        re_path(r'^address/$', AddressView.as_view(), name='core_tenant_address'),


    ]))
]