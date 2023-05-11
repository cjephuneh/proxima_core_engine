from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from core_engine_chat_app.models import Chat

class CountAllHourlyChats(APIView):

    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        start_time = timezone.now() - timezone.timedelta(hours=1)
        end_time = timezone.now()

        chat_count = Chat.objects.filter(tenant_id=tenant, date_time_created_at__gte=start_time, date_time_created_at__lt=end_time).count()

        return JsonResponse({'total_chats_last_hour': chat_count}, status=status.HTTP_200_OK)
