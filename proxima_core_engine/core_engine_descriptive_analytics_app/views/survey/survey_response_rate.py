from django.http import HttpResponse, JsonResponse
from core_engine_survey_app.models import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_tenant_users_app.models import Client

class SurveyResponseRate(APIView):

    def get(self, request):
        survey_id = self.request.query_params.get('survey_id')

        if not survey_id:
            return JsonResponse({'error': 'No survey ID provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the total number of clients in the target audience
        target_audience_count = Client.objects.filter(survey__survey_id=survey_id).count()

        # Get the number of clients who responded to the survey
        responded_count = Response.objects.filter(survey_id=survey_id).distinct('client').order_by('client').count()

        # Calculate the response rate as a percentage
        response_rate = (responded_count / target_audience_count) * 100 if target_audience_count > 0 else 0

        # Return the result as a JSON response
        data = {'response_rate': response_rate}
        return JsonResponse(data, status=status.HTTP_200_OK)


