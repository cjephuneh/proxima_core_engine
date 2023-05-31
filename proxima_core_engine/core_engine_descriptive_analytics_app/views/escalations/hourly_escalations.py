from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound

class CountHourlyEscalatedIssues(APIView):
    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        with connection.cursor() as cursor:
            query = """
                SELECT count(*) FROM core_engine_chat_app_Message
                WHERE date_time_created_at >= date_trunc('hour', now()) - INTERVAL '1 hour'
                    AND date_time_created_at < date_trunc('hour', now())
                    AND escalated = True
                    AND core_engine_chat_app_Message.chat_id_id IN (
                        SELECT core_engine_chat_app_Chat.chat_id
                        FROM core_engine_chat_app_Chat
                        WHERE tenant_id = %s
                    )
            """
            cursor.execute(query, [tenant])
            row = cursor.fetchone()
        
        data = {
            'count': row[0],
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
