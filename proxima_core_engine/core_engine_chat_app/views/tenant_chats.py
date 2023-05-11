import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_chat_app.models import TenantChats
from core_engine_chat_app.serializers import TenantChatsSerializer
from core_engine_chat_app.utils import save_tenant_chat
from core_engine_utils_app.views import get_filter_from_params


log = logging.getLogger(__name__)


class TenantChatsView(APIView):
    """
    TenantChatss API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve TenantChatss matching query.

        Params:
        tenant_chats_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'tenant_chats_id': 'tenant_chats_id',
            'tenant_id': 'tenant_id',
        }
        filters = get_filter_from_params(params, allowed_params)

        tenant_chat_query = TenantChats.objects.prefetch_related('tenant').filter(**filters)
        tenant_chat_set = TenantChatsSerializer(tenant_chat_query, many=True)
        return Response(tenant_chat_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add a Chat to the database.

        Params:
        tenant_chats_id
        tenant_id
        """
        tenant_chat, created = save_tenant_chat(**request.data)
        if not tenant_chat:
            return Response(status=400)
        
        tenant_chat_info = TenantChatsSerializer(tenant_chat)
        if created:
            return Response(tenant_chat_info.data, status=201)
        else:
            return Response(tenant_chat_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a chat from the database.

        Params (all required):
        tenant_chats_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'tenant_chats_id': 'tenant_chats_id',
            'tenant_id': 'tenant_id',
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        tenant_chat_query = TenantChats.objects.prefetch_related('tenant').filter(**filters)
        delete_count, delete_type = tenant_chat_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)