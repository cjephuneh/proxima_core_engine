import logging
from rest_framework import serializers

from core_engine_chat_app.models import (
    Chat, ClientChats, Message, TenantChats
)

from core_engine_tenant_users_app.models import (
    Client
)

from core_engine_tenant_management_app.models import (
    Tenant
)
# Chat serializers

class TenantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['tenant_id', 'tenant_name']

class ClientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ChatSerializer(serializers.ModelSerializer):
    # tenant = serializers.CharField(
    #     source='core_engine_tenant_management_app.tenant', default=None
    # )
    # guest_client = serializers.CharField(
    #     source='core_engine_tenant_users_app.client', default=None
    # )
    # chat_owner = serializers.CharField(
    #     source='core_engine_tenant_users_app.client', default=None
    # )
    tenant_id = TenantInfoSerializer(many=False)
    chat_owner = ClientInfoSerializer(many=False)
    guest_client = ClientInfoSerializer(many=False)
    class Meta:
        model = Chat
        fields = ('chat_id', 'tenant_id', 'guest_client', 'chat_owner', 'client_satisfaction')
        # read_only_fields = fields


# Messages serializers

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('message_id', 'chat_id', 'text_content', 'voice_content', 'message_sender','escalated', 'channel', 'topic')
        # read_only_fields = ('position',)


class ClientChatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientChats
        fields = (
            'client_chats_id', 'client_id', 'chat_id'
        )
        depth = 1


class TenantChatsSerializer(serializers.ModelSerializer):
    tenant_id = serializers.CharField(
        source='core_engine_tenant_management_app.tenant', default=None
    )
    chat_id = serializers.CharField(
        source='core_engine_chat_app.chat', default=None
    )
    class Meta:
        model = TenantChats
        fields = (
            'tenant_chats_id', 'tenant_id', 'chat_id'
        )
        depth = 1