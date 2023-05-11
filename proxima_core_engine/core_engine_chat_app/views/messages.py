import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_chat_app.models import Message
from core_engine_chat_app.serializers import MessageSerializer
from core_engine_chat_app.utils import save_chat_message
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class MessageView(APIView):
    """
    Messages API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Messages matching query.

        Params:
        message_id
        chat_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'message_id': 'message_id',
            'chat_id': 'chat_id',
        }
        filters = get_filter_from_params(params, allowed_params)

        message = Message.objects.select_related('chat_id').filter(**filters)
        message = MessageSerializer(message, many=True)
        return Response(message.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Chat to the database.

        Params:
        message_id
        chat_id
        """
        message, created = save_chat_message(**request.data)
        if not message:
            return Response(status=400)
        
        message_info = MessageSerializer(message)
        if created:
            return Response(message_info.data, status=201)
        else:
            return Response(message_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a chat from the database.

        Params (all required):
        message_id
        chat_id
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'message_id': 'message_id',
            'chat_id': 'chat_id',
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        message_query = Message.objects.prefetch_related('message').filter(**filters)
        delete_count, delete_type = message_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)