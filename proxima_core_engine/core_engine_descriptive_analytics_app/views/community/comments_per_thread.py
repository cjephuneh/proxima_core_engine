from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
    

class AverageCommentsPerThread(APIView):

    def get(self, request):
        community_id = self.request.query_params.get('community')

        if not community_id:
            return JsonResponse({'error': 'No Community provided'}, status=status.HTTP_400_BAD_REQUEST)
        

        with connection.cursor() as cursor:
            # Count the number of threads and comments for the given community
            query = """
                SELECT COUNT(DISTINCT t.thread_id), COUNT(c.comment_id)
                FROM core_engine_community_app_thread t
                LEFT JOIN core_engine_community_app_issue i ON t.issue_id = i.issue_id
                LEFT JOIN core_engine_community_app_comment c ON t.thread_id = c.thread_id
                WHERE i.community_id_id = %s
            """
            cursor.execute(query, [community_id])
            row = cursor.fetchone()
            thread_count, comment_count = row

        # Calculate the average number of comments per thread
        avg_comments_per_thread = comment_count / thread_count if thread_count > 0 else 0

        # Return the result as a JSON response
        data = {'avg_comments_per_thread': avg_comments_per_thread}
        return JsonResponse(data, status=status.HTTP_200_OK)

