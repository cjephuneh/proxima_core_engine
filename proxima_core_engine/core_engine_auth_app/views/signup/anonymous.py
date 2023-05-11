import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_tenant_users_app.serializers import AnonymousUserSerializer
from core_engine_auth_app.utils import save_anonymous_user
from core_engine_utils_app.views import get_filter_from_params
from core_engine_tenant_users_app.models import AnonymousUser

log = logging.getLogger(__name__)



class AnonymousUserView(APIView):
    """
    AnonymousUsers API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve AnonymousUsers matching query.

        Params:
        contact

        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'contact': 'contact',

        }
        filters = get_filter_from_params(params, allowed_params)

        anonymoususer_query = AnonymousUser.objects.prefetch_related('anonymoususer').filter(**filters)
        anonymoususer_set = AnonymousUserSerializer(anonymoususer_query, many=True)
        return Response(anonymoususer_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a anonymous to the database.

        Params:
        contact

        """
        anonymoususer, created = save_anonymous_user(**request.data)
        if not anonymoususer:
            return Response(status=400)
        
        anonymoususer_info = AnonymousUserSerializer(anonymoususer)
        if created:
            return Response(anonymoususer_info.data, status=201)
        else:
            return Response(anonymoususer_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a anonymoususer from the database.

        Params (all required):
        contact

        """
        # Validate params args
        params = request.query_params
        required_params = {
            'contact': 'contact'
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        anonymoususer_query = AnonymousUser.objects.prefetch_related('anonymoususer').filter(**filters)
        delete_count, delete_type = anonymoususer_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)