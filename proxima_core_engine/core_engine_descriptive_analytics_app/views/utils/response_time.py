from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection


class AverageResponseTime(APIView):

    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            query = """
            SELECT chat_id_id, 
                   AVG(extract(epoch from (updated_at - sent_at)) / 60) as avg_response_time
            FROM core_engine_chat_app_message 
            WHERE date_time_created_at >= date_trunc('hour', now()) - INTERVAL '1 hour'  
                  AND date_time_created_at < date_trunc('hour', now()) 
                  AND chat_id_id IN (
                      SELECT chat_id 
                      FROM core_engine_chat_app_chat 
                      WHERE tenant_id = %s
                  ) 
            GROUP BY chat_id_id
            """ % tenant
            cursor.execute(query)
            rows = cursor.fetchall()

        response_data = {}
        for row in rows:
            chat_id = row[0]
            avg_response_time = row[1]
            response_data[chat_id] = {'avg_response_time': avg_response_time}

        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
class HourlyAverageResponseTime(APIView):

    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            query = """
            SELECT chat_id_id, 
                   AVG(extract(epoch from (updated_at - sent_at)) / 60) as avg_response_time
            FROM core_engine_chat_app_message 
            WHERE date_time_created_at >= date_trunc('hour', now()) - INTERVAL '1 hour'  
                  AND date_time_created_at < date_trunc('hour', now()) 
                  AND chat_id_id IN (
                      SELECT chat_id 
                      FROM core_engine_chat_app_chat 
                      WHERE tenant_id = %s
                  ) 
            GROUP BY chat_id_id
            """ % tenant
            cursor.execute(query)
            rows = cursor.fetchall()

        response_data = {}
        for row in rows:
            chat_id = row[0]
            avg_response_time = row[1]
            response_data[chat_id] = {'avg_response_time': avg_response_time}

        return JsonResponse(response_data, status=status.HTTP_200_OK)
