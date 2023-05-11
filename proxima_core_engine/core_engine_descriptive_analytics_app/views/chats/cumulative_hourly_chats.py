from datetime import datetime, timedelta
from django.db.models import Count
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from core_engine_chat_app.models import Chat

class CumulativeCountAllHourlyChats(APIView):
    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        hourly_cumulative_engagement = []
        now = datetime.now()
        for i in range(24):
            start = now - timedelta(hours=i+1)
            end = now - timedelta(hours=i)

            chats = Chat.objects.filter(
                tenant_id=tenant_id,
                created_at__gte=start.replace(minute=0, second=0),
                created_at__lt=end.replace(minute=0, second=0),
            ).aggregate(count=Count('chat_id'))

            hourly_cumulative_engagement.append({
                "start_time": start.replace(minute=0, second=0).isoformat(),
                "end_time": end.replace(minute=0, second=0).isoformat(),
                "count": chats['count']
            })

        return JsonResponse(hourly_cumulative_engagement, safe=False, status=status.HTTP_200_OK)
