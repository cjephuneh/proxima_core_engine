import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_survey_app.models import Response as SurveyResponse
from core_engine_survey_app.serializers import ResponseSerializer
from core_engine_survey_app.utils import save_client_survey_response
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class ResponseView(APIView):
    """
    Response API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve response matching query.

        Params:
        response_id
        survey_id
        client
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'response_id': 'response_id',
            'survey_id': 'survey_id',
            'client': 'client'
        }
        filters = get_filter_from_params(params, allowed_params)

        response_query = SurveyResponse.objects.prefetch_related('survey_id', 'client').filter(**filters)
        response_set = ResponseSerializer(response_query, many=True)
        return Response(response_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a survey to the database.

        Params:
        response_id
        survey_id
        client
        survey_response
        """
        response, created = save_client_survey_response(**request.data)
        if not created:
            return Response({'error': 'Failed to capture response'}, status=400)
        
        response_info = ResponseSerializer(response)
        if created:
            return Response(response_info.data, status=201)
        # else:
        #     return Response(response_info.data, status=200)


