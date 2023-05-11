from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from core_engine_community_app.models import Issue

class IssueUserRelation(APIView):
    
    def get(self, request):
        community_id = self.request.query_params.get('community')
        
        if not community_id:
            return Response({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get unique clients who raised an issue in the given community
        unique_clients = Issue.objects.filter(community_id=community_id).\
            values('client_id').annotate(num_issues=Count('client_id'))
        
        total_unique_users = len(unique_clients)
        data = {'count': total_unique_users}
        return Response(data, status=status.HTTP_200_OK)
