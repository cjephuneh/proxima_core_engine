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

        # Count the number of chats for each client and calculate the average client_satisfaction for each client
        qs = Chat.objects.filter(tenant_id=tenant_id).values('guest_client').annotate(chat_count=Count('guest_client'), satisfaction=Avg('client_satisfaction'))

        # Calculate the overall client_satisfaction percentage for the tenant
        num_chats = Chat.objects.filter(tenant_id=tenant_id).count()
        satisfaction_percentage = 0
        if num_chats > 0:
            satisfaction_percentage = (Chat.objects.filter(tenant_id=tenant_id, client_satisfaction=True).count() / num_chats) * 100

        # Return the results as JSON
        data = {
            'client_satisfaction_percentage': satisfaction_percentage,
            'client_satisfaction_by_client': qs,
        }
        return Response(data, status=status.HTTP_200_OK)

# class ClientHourlyClientSatisfaction(APIView):

#     def get(self, request):

#         tenant = self.request.query_params['tenant']

#         with connection.cursor() as cursor:
#             query = "SELECT core_engine_chat_app_Chat.client_satisfaction FROM core_engine_chat_app_Chat WHERE tenant_id = %s AND date_time_created_at >= date_trunc('hour', now()) - INTERVAL '1 hour'  AND date_time_created_at < (date_trunc('hour', now()))"% tenant
#             cursor.execute(query)
#             row = cursor.fetchall()
#         print(row)

#         return HttpResponse(row, content_type='application/json')


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
