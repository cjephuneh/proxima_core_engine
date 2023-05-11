from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from core_engine_survey_app.models import Survey
from django.db.models import Avg

from django.db.models import Avg, ExpressionWrapper, F
from django.db.models.fields import DateField

class AverageSurveyRunPeriod(APIView):

    def get(self, request):
        tenant_id = self.request.query_params.get('tenant_id')

        if not tenant_id:
            return JsonResponse({'error': 'No tenant_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        avg_survey_period = Survey.objects.filter(tenant_id=tenant_id).aggregate(
            avg_period=Avg(ExpressionWrapper(F('end_day') - F('start_day'), output_field=DateField()))
        )

        # Return the result as a JSON response
        data = {'avg_survey_period': avg_survey_period.get('avg_period', 0)}
        return JsonResponse(data, status=status.HTTP_200_OK)

