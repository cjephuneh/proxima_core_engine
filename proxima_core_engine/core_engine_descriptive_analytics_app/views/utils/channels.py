from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection

# CommunicationChannel
class CommunicationChannels(APIView):

    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        mobile_count = "SELECT count(*) FROM core_engine_chat_app_Message WHERE channel ='Mobile' AND core_engine_chat_app_Message.chat_id_id IN (SELECT core_engine_chat_app_Chat.chat_id FROM core_engine_chat_app_Chat WHERE tenant_id_id = %s)" % tenant

        website_count = "SELECT count(*) FROM core_engine_chat_app_Message WHERE channel ='Website' AND core_engine_chat_app_Message.chat_id_id IN (SELECT core_engine_chat_app_Chat.chat_id FROM core_engine_chat_app_Chat WHERE tenant_id_id = %s)" % tenant

        communication_channels = {'mobile_count': 0, 'website_count': 0}

        with connection.cursor() as cursor:
            cursor.execute(mobile_count)
            mobile_count_result = cursor.fetchone()[0]
            communication_channels['mobile_count'] = mobile_count_result

            cursor.execute(website_count)
            website_count_result = cursor.fetchone()[0]
            communication_channels['website_count'] = website_count_result

        return JsonResponse(communication_channels, status=status.HTTP_200_OK)
