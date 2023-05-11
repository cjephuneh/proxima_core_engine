from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from core_engine_chat_app.models import Chat


class CountAllChats(APIView):

    def get(self, request):
        tenant_id = self.request.query_params.get('tenant')

        if not tenant_id:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        chats = Chat.objects.filter(tenant_id=tenant_id)

        chat_count = len(chats)

        data = {'chat_count': chat_count}

        return JsonResponse(data, status=status.HTTP_200_OK)

