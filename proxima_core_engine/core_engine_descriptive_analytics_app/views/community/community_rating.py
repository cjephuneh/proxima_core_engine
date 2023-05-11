from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db import models
from core_engine_community_app.models import Rating


 
"""
All people who rate the community will have the ratings scored then the average will be found here.
"""
class CommunityRating(APIView):

    def get(self, request):

        community_id = self.request.query_params.get('community')

        if not community_id:
            return Response({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)

        ratings = Rating.objects.filter(community_id=community_id)
        count = ratings.aggregate(models.Avg('rating')).get('rating__avg') or 0

        return JsonResponse({'count': round(count, 1)}, safe=False, status=status.HTTP_200_OK)
