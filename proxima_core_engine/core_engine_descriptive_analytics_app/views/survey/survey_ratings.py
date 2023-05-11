from django.http import HttpResponse, JsonResponse
# from rest_framework.response import Response
from core_engine_survey_app.models import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
    

class SurveyRatings(APIView):

    def get(self, request):
        # Get all responses

        survey_id = self.request.query_params.get('survey_id')
        responses = Response.objects.filter(survey_id=survey_id)

        # Aggregate survey ratings
        survey_ratings = {}
        for response in responses:
            survey_id = response.survey_id_id
            survey_type = response.survey_id.survey_type

            # If the survey is open-ended, ignore it
            # if survey_type == 'open_ended':
            #     continue

            survey_response = response.survey_response
            if survey_id in survey_ratings:
                survey_ratings[survey_id].append(survey_response)
            else:
                survey_ratings[survey_id] = [survey_response]

        # Calculate the average survey rating for each survey
        # Calculate the average survey rating for each survey
        survey_avg_ratings = {}
        for survey_id, ratings in survey_ratings.items():
            non_null_ratings = [rating for rating in ratings if rating is not None]
            if non_null_ratings:
                avg_rating = sum(non_null_ratings) / len(non_null_ratings)
                survey_avg_ratings[survey_id] = avg_rating
            else:
                survey_avg_ratings[survey_id] = None


        # Return the survey ratings as a JSON response
        return JsonResponse(survey_avg_ratings, status=status.HTTP_200_OK)


