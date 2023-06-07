import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_survey_app.models import Survey
from core_engine_survey_app.serializers import SurveySerializer
from core_engine_survey_app.utils import save_tenant_survey
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class SurveyView(APIView):
    """
    Survey API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Chats matching query.

        Params:
        survey_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'survey_id': 'survey_id',
            'tenant_id': 'tenant_id'
        }

        # make sure tenant_id is passed
        if not params.get('tenant_id'):
            return Response({"error": "tenant_id missing"}, status=400)

        filters = get_filter_from_params(params, allowed_params)

        survey_query = Survey.objects.prefetch_related('tenant_id', 'target_audience').filter(**filters)
        survey_set = SurveySerializer(survey_query, many=True)
        response = {'error': False, 'data': survey_set.data}
        return Response(response, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Survey to the database.

        Params:
        survey_id
        tenant_id
        survey_topic
        survey_description
        survey_context
        survey_questions
        target_audience
        """
        survey, created = save_tenant_survey(**request.data)
        if not created:
            return Response({'error': 'Failed to create survey'},status=400)
        
        survey_info = SurveySerializer(survey)
        if created:
            return Response(survey_info.data, status=201)
        # else:
        #     return Response(survey_info.data, status=200)

