from django.db.models import Avg, Count
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from core_engine_chat_app.models import Chat, Message

class AverageVoiceMessagePerchat(APIView):

    def get(self, request):
        tenant = self.request.query_params.get('tenant')

        if not tenant:
            return JsonResponse({'error': 'No tenant provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all chats and their non-null voice messages for the given tenant
        chats = Chat.objects.filter(tenant_id=tenant)
        voice_messages = Message.objects.filter(chat_id__in=chats, voice_content__isnull=False)

        # Calculate the average number of non-null voice messages per chat
        avg_voice_messages = voice_messages.values('chat_id').annotate(num_voice_messages=Count('chat_id_id')).aggregate(Avg('num_voice_messages'))

        return JsonResponse({'average_voice_messages_per_chat': avg_voice_messages['num_voice_messages__avg']}, status=status.HTTP_200_OK)
