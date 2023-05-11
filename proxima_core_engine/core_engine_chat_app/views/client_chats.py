import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_chat_app.models import ClientChats
from core_engine_chat_app.serializers import ClientChatsSerializer
from core_engine_chat_app.utils import save_client_chats
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class ClientChatsView(APIView):
    """
    ClientChatss API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve ClientChatss matching query.

        Params:
        client_chats_id
        client_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'client_chats_id': 'client_chats_id',
            'client_id': 'client_id',
        }
        filters = get_filter_from_params(params, allowed_params)

        client_chat_query = ClientChats.objects.prefetch_related('clientchats').filter(**filters)
        client_chat_set = ClientChatsSerializer(client_chat_query, many=True)
        return Response(client_chat_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Chat to the database.

        Params:
        client_chats_id
        client_id
        """
        client_chat, created = save_client_chats(**request.data)
        if not client_chat:
            return Response(status=400)
        
        client_chat_info = ClientChatsSerializer(client_chat)
        if created:
            return Response(client_chat_info.data, status=201)
        else:
            return Response(client_chat_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a chat from the database.

        Params (all required):
        client_chats_id
        client_id
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'client_chats_id': 'client_chats_id',
            'client_id': 'client_id',
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        client_chat_query = ClientChats.objects.prefetch_related('client').filter(**filters)
        delete_count, delete_type = client_chat_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)