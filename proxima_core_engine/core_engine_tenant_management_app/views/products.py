import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_tenant_management_app.models import Product
from core_engine_tenant_management_app.serializers import ProductSerializer

from core_engine_utils_app.views import get_filter_from_params
from core_engine_tenant_management_app.utils import save_tenant_product


log = logging.getLogger(__name__)


class ProductView(APIView):
    """
    Product API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve products matching query.

        Params:
        product_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'product_id': 'product_id',
            'tenant_id': 'tenant_id',
        }
        filters = get_filter_from_params(params, allowed_params)

        product_query = Product.objects.prefetch_related('tenant').filter(**filters)
        product_set = ProductSerializer(product_query, many=True)
        return Response(product_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Product to the database.

        Params:
        product_id
        tenant_id
        name (optional)
        description
        price
        """
        product, created = save_tenant_product(**request.data)
        if not product:
            return Response(status=400)
        
        product_info = ProductSerializer(product)
        if created:
            return Response(product_info.data, status=201)
        else:
            return Response(product_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a Product from the database.

        Params (all required):
        product_id
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'product_id': 'product_id'        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        product_query = Product.objects.prefetch_related('tenant').filter(**filters)
        delete_count, delete_type = product_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)