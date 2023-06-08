from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection

class MostPopularTopics(APIView):

    def get(self, request):

        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Execute the SQL query to get the most popular topics
        with connection.cursor() as cursor:
            query = """
                SELECT topic, COUNT(*) AS topic_count
                FROM core_engine_chat_app_message
                INNER JOIN core_engine_chat_app_chat ON core_engine_chat_app_message.chat_id_id = core_engine_chat_app_chat.chat_id
                WHERE core_engine_chat_app_chat.tenant_id_id = %s
                GROUP BY topic
                ORDER BY topic_count DESC
            """
            cursor.execute(query, [tenant_id])
            rows = cursor.fetchall()

        # Return the count and names of the most popular topics
        data = [{'topic': row[0], 'count': row[1]} for row in rows]
        return JsonResponse({'data': data}, status=status.HTTP_200_OK)
