import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_tenant_management_app.models import Metadata
from core_engine_tenant_management_app.serializers import MetadataSerializer

from core_engine_utils_app.views import get_filter_from_params
from core_engine_tenant_management_app.utils import save_tenant_metadata



log = logging.getLogger(__name__)


class MetadataView(APIView):
    """
    Metadatas API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Metadata matching query.

        Params:
        metadata_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'metadata_id': 'metadata_id',
            'tenant_id': 'tenant_id'
                            }
        filters = get_filter_from_params(params, allowed_params)

        metadata_query = Metadata.objects.prefetch_related('tenant').filter(**filters)
        metadata_set = MetadataSerializer(metadata_query, many=True)
        return Response(metadata_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a metadata to the database.

        Params:
        metadata_id
        tenant_id
        """
        metadata, created = save_tenant_metadata(**request.data)
        if not Metadata:
            return Response(status=400)
        
        metadata_info = MetadataSerializer(metadata)
        if created:
            return Response(metadata_info.data, status=201)
        else:
            return Response(metadata_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a metadata of a tenant from the database.

        Params (all required):
         metadata_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'metadata_id': 'metadata_id',
            'tenant_id': 'tenant_id'
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        metadata_query = Metadata.objects.prefetch_related('tenant').filter(**filters)
        delete_count, delete_type = metadata_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)