from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from rest_framework.exceptions import ValidationError

class CumulativeVoiceMessages(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        with connection.cursor() as cursor:
            query = """
                SELECT SUM(LENGTH(voice_content)) 
                FROM core_engine_chat_app_Message 
                INNER JOIN core_engine_chat_app_Chat 
                ON core_engine_chat_app_Message.chat_id_id = core_engine_chat_app_Chat.chat_id 
                WHERE core_engine_chat_app_Chat.tenant_id = %s 
            """
            cursor.execute(query, [tenant_id])
            row = cursor.fetchone()
            total_voice_size = row[0] or 0  # handle case where sum is null
        return JsonResponse({'total_voice_size': total_voice_size}, status=status.HTTP_200_OK)

