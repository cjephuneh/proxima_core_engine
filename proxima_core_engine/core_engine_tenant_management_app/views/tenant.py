import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_tenant_management_app.models import Tenant
from core_engine_tenant_management_app.serializers import TenantSerializer

from core_engine_utils_app.views import get_filter_from_params
from core_engine_tenant_management_app.utils import save_tenant

log = logging.getLogger(__name__)


class TenantView(APIView):
    """
    Tenant API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Tenant matching query.

        Params:
        tenant_id
        tenant_name
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'tenant_id': 'tenant_id',
            'tenant_name': 'tenant_name',
        }
        filters = get_filter_from_params(params, allowed_params)

        tenant_query = Tenant.objects.prefetch_related('tenant').filter(**filters)
        tenant_set = TenantSerializer(tenant_query, many=True)
        return Response(tenant_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Tenant to the database.

        Params:
        tenant_id
        name (optional)
        """
        tenant, created = save_tenant(**request.data)
        if not tenant:
            return Response(status=400)
        
        tenant_info = TenantSerializer(tenant)
        if created:
            return Response(tenant_info.data, status=201)
        else:
            return Response(tenant_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a tenant from the database.

        Params (all required):
        tenant_id
        tenant_name
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'tenant_id': 'course_id',
            'org': 'tenant_name'
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        tenant_query = Tenant.objects.prefetch_related('tenant').filter(**filters)
        delete_count, delete_type = tenant_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)