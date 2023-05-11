from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_community_app.models import Comment
from django.db.models import Count, Sum

    
"""
All new users who are commenting on thechat
"""

class UniqueComments(APIView):

    def get(self, request):
        community = self.request.query_params.get('community')
        if not community:
            return Response({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)

        if community is not None:
            unique_comments_count = Comment.objects.filter(thread__issue__community_id=community).values('client').annotate(total=Count('client_id', distinct=True)).aggregate(sum=Sum('total'))['sum']

            if unique_comments_count is not None:
                serialized_comments = serialize('json', unique_comments_count)
                return Response(serialized_comments, content_type='application/json', status=status.HTTP_200_OK)
            else:
                return Response({"error": "No unique comments found for the given community"}, status=status.HTTP_200_OK, content_type='application/json')
        else:
            return Response({"error": "Missing 'community' parameter in the request"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')




