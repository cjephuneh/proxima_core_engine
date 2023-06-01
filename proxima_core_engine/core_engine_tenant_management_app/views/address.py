import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_tenant_management_app.models import Address
from core_engine_tenant_management_app.serializers import AddressSerializer

from core_engine_utils_app.views import get_filter_from_params
from core_engine_tenant_management_app.utils import save_tenant_address


log = logging.getLogger(__name__)


class AddressView(APIView):
    """
    Addresss API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Addresss matching query.

        Params:
        address_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'address_id': 'address_id',
            'tenant_id': 'tenant_id',
        }
        filters = get_filter_from_params(params, allowed_params)

        address_query = Address.objects.prefetch_related('tenant_id').filter(**filters)
        address_set = AddressSerializer(address_query, many=True)
        return Response(address_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a tenant address to the database.

        Params:
        address_id
        tenant_id
        """
        address, created = save_tenant_address(**request.data)
        if not created:
            return Response({'error': 'Failed to save tenant address'}, status=400)
        
        address_info = AddressSerializer(address)
        if created:
            return Response(address_info.data, status=201)
        # else:
        #     return Response(address_info.data, status=200)


    