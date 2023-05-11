import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_survey_app.models import SurveySubGroups
from core_engine_survey_app.serializers import SurveySubGroupsSerializer
from core_engine_survey_app.utils import save_survey_subgroup
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class SurveySubGroupsView(APIView):
    """
    Survey API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Chats matching query.

        Params:
        survey_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'survey_id': 'survey_id',
        }
        filters = get_filter_from_params(params, allowed_params)

        survey_subgroup_report_query = SurveySubGroups.objects.select_related('survey_id').filter(**filters)
        survey_subgroup_report_set = SurveySubGroupsSerializer(survey_subgroup_report_query, many=True)
        return Response(survey_subgroup_report_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Survey Subgroup to the database.

        Params:
        survey_subgroups_id
        survey_id
        subgroup_name
        subgroup_description
        subgroup_clients
        """
        surveysubgroups, created = save_survey_subgroup(**request.data)
        if not surveysubgroups:
            return Response(status=400)
        
        surveysubgroups_info = SurveySubGroupsSerializer(surveysubgroups)
        if created:
            return Response(surveysubgroups_info.data, status=201)
        else:
            return Response(surveysubgroups_info.data, status=200)

