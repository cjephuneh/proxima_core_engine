from rest_framework.response import Response
import datetime
from rest_framework.views import APIView
from rest_framework import status
from django.core.serializers import serialize
from django.db import connection
from core_engine_chat_app.models import Chat
from django.db.models.functions import TruncMonth
from django.db.models import Count

class EngagementFrequency(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return Response({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all chats for the specified tenant
        chats = Chat.objects.filter(tenant_id=tenant_id)

        # Aggregate the chats by month and count the number of chats per month
        chats_by_month = chats.annotate(month=TruncMonth('date_time_created_at')).values('month').annotate(count=Count('chat_id'))

        # Create a dictionary to hold the chat count for each month
        chat_count_dict = {}
        for chat in chats_by_month:
            chat_count_dict[chat['month'].strftime('%B')] = chat['count']

        # Create a list of dictionaries, with each dictionary holding the chat count for a month
        general_engagement = []
        for month in range(1, 13):
            month_name = datetime.date(2022, month, 1).strftime('%B')
            chat_count = chat_count_dict.get(month_name, 0)
            general_engagement.append({'month': month_name, 'count': chat_count})

        return Response(general_engagement, status=status.HTTP_200_OK)

