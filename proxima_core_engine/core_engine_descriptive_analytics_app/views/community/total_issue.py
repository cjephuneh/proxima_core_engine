from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_community_app.models import Issue

"""
All the issues raised for a particular community
"""

class CumulativeIssues(APIView):
    
    def get(self, request):
        community_id = self.request.query_params.get('community')
        if not community_id:
            return Response({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the count of issues for the specified community.
        count = Issue.objects.filter(community_id=community_id).count()
        
        return Response({'count': count}, status=status.HTTP_200_OK)
