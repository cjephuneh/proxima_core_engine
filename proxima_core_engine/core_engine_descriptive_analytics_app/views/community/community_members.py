from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_community_app.models import Community

    
class CommunityMembers(APIView):

    def get(self, request):

        community_id = self.request.query_params.get('community')

        if not community_id:
            return Response({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        member_count = community.members.count()

        data = {
            'community': community.community_name,
            'member_count': member_count
        }

        return JsonResponse(data, status=status.HTTP_200_OK)
