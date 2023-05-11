from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
    
"""
All the new commenbts on a particular thread
"""

class CumulativeComments(APIView):
    def get(self, request):
        community = self.request.query_params.get('community')
        if not community:
            return Response({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            query = """
                SELECT count(*) 
                FROM core_engine_community_app_Comment 
                JOIN core_engine_community_app_Thread ON core_engine_community_app_Thread.thread_id = core_engine_community_app_Comment.thread_id
                WHERE core_engine_community_app_Thread.issue_id IN (
                    SELECT core_engine_community_app_Issue.community_id_id 
                    FROM core_engine_community_app_Issue 
                    WHERE community_id_id = %s
                )
            """ % community
            cursor.execute(query)
            row = cursor.fetchone()
            count = row[0]

        return Response({'count': count}, status=status.HTTP_200_OK)

