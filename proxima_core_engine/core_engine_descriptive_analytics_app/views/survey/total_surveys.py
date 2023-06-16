from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_survey_app.models import Survey

class TotalSurveys(APIView):

    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return JsonResponse({'error': 'No Tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Count the number of surveys for the given tenant
        survey_count = Survey.objects.filter(tenant_id=tenant_id).count()

        # Return the survey count as a JSON response
        data = {'survey_count': survey_count}
        return JsonResponse(data, status=status.HTTP_200_OK)


