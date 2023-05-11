import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_survey_app.models import SurveyReport
from core_engine_survey_app.serializers import SurveyReportSerializer
from core_engine_survey_app.utils import save_survey_report
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class SurveyReportView(APIView):
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

        survey_report_query = SurveyReport.objects.select_related('survey_id').filter(**filters)
        survey_report_set = SurveyReportSerializer(survey_report_query, many=True)
        return Response(survey_report_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Survey to the database.

        Params:
        survey_report_id
        survey_id
        conclusion
        survey_success
        survey_reporter
        """
        surveyreport, created = save_survey_report(**request.data)
        if not surveyreport:
            return Response(status=400)
        
        surveyreport_info = SurveyReportSerializer(surveyreport)
        if created:
            return Response(surveyreport_info.data, status=201)
        else:
            return Response(surveyreport_info.data, status=200)

