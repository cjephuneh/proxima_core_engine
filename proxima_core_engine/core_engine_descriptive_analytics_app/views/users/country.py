from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection



class CountryDistribution(APIView):

    def get(self, request):

        tenant_id = request.query_params.get('tenant')
        if not tenant_id:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            query = """
                SELECT core_engine_users_profile_app_ClientProfile.country
                FROM core_engine_chat_app_Chat
                JOIN core_engine_users_profile_app_ClientProfile ON core_engine_chat_app_Chat.chat_owner_id = core_engine_users_profile_app_ClientProfile.client_id
                WHERE core_engine_chat_app_Chat.tenant_id = %s
            """
            cursor.execute(query, [tenant_id])
            rows = cursor.fetchall()
            countries = [row[0] for row in rows]

        return Response({"countries": countries}, status=status.HTTP_200_OK)
