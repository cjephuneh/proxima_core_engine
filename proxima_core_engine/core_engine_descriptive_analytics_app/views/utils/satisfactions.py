from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_chat_app.models import Chat    
from django.db.models import Count, Avg
from django.http import JsonResponse

class ClientSatisfaction(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # get all chats for the given tenant that were created in the last hour
        chats = Chat.objects.filter(
            tenant_id=tenant_id,

        )

        # count the number of chats where the client is satisfied
        satisfied_chats_count = chats.filter(client_satisfaction=True).count()

        # calculate the satisfaction percentage
        if chats.count() > 0:
            satisfaction_percentage = satisfied_chats_count / chats.count() * 100
        else:
            satisfaction_percentage = 0

        return JsonResponse({'satisfaction_percentage': satisfaction_percentage}, status=status.HTTP_200_OK)


from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from core_engine_chat_app.models import Chat

class ClientHourlyClientSatisfaction(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # get all chats for the given tenant that were created in the last hour
        chats = Chat.objects.filter(
            tenant_id=tenant_id,
            date_time_created_at__gte=timezone.now() - timezone.timedelta(hours=1),
            date_time_created_at__lt=timezone.now()
        )

        # count the number of chats where the client is satisfied
        satisfied_chats_count = chats.filter(client_satisfaction=True).count()

        # calculate the satisfaction percentage
        if chats.count() > 0:
            satisfaction_percentage = satisfied_chats_count / chats.count() * 100
        else:
            satisfaction_percentage = 0

        return JsonResponse({'satisfaction_percentage': satisfaction_percentage}, status=status.HTTP_200_OK)
