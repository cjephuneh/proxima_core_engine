import logging
import whisper
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_chat_app.models import Chat
from core_engine_chat_app.serializers import ChatSerializer
from core_engine_chat_app.utils import save_tenant_client_chat
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class ChatView(APIView):
    """
    Chats API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Chats matching query.

        Params:
        chat_id
        tenant
        chat_owner
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'chat_id': 'chat_id',
            'tenant': 'tenant',
            'chat_owner': 'chat_owner'
        }
        filters = get_filter_from_params(params, allowed_params)

        chat_query = Chat.objects.select_related('tenant').filter(**filters)
        chat_set = ChatSerializer(chat_query, many=True)
        return Response(chat_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Chat to the database.

        Params:
        chat_id
        tenant_id
        """
        chat, created = save_tenant_client_chat(**request.data)
        if not chat:
            return Response(status=400)
        
        chat_info = ChatSerializer(chat)
        if created:
            return Response(chat_info.data, status=201)
        else:
            return Response(chat_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a chat from the database.

        Params (all required):
        chat_id
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'chat_id': 'chat_id',
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        chat_query = Chat.objects.prefetch_related('chat').filter(**filters)
        delete_count, delete_type = chat_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)
    

class VoiceNoteAPIView(APIView):
    audio_file = 'recording.webm'
    model = whisper.load_model('small.en')

    
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio')
        audio = self.whisper.load_audio(audio_file) 
        result = self.model.transcribe(audio, fp16=False)
        text = result["text"]
        return Response(text, status=200)
    