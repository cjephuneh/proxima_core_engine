import logging
from rest_framework import serializers

from core_engine_community_app.models import (
    Comment, Community, Issue, Thread
)
from core_engine_tenant_users_app.models import (
    Client
)
# Comment serializers

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_id', 'thread', 'client', 'comment_description', 'likes', 'dislikes')
        # read_only_fields = fields

"""
Community serializers
"""
# Community serializers

class CommunitySerializer(serializers.ModelSerializer):
    tenant_id = serializers.CharField(
        source='core_engine_tenant_management_app.tenant', default=None
    )
    class Meta:
        model = Community
        fields = ('community_id', 'tenant_id', 'description')
        # read_only_fields = ('position',)

#Join a particular community
class JoinCommunitySerializer(serializers.ModelSerializer):
    """serializers that enable a user to join a particular comunity
    ."""
    client = serializers.CharField(
        source='core_engine_tenant_users_app.client', default=None
    )
    class Meta:
        model = Community
        fields = ['client',]

 
    def create(self, validated_data):
        return Community.objects.add_client_to_community(**validated_data)
    
#Join a particular community
class LeaveCommunitySerializer(serializers.ModelSerializer):
    """serializers that enable a user to join a particular comunity
    ."""
    client = serializers.CharField(
        source='core_engine_tenant_users_app.client', default=None
    )
    class Meta:
        model = Community
        fields = ['client',]

 
    def create(self, validated_data):
        return Community.objects.remove_client_from_community(**validated_data)
    

class IssueSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(
        source='core_engine_tenant_users_app.client', default=None
    )
    community_id = serializers.CharField(
        source='core_engine_community_app.community', default=None
    )
    class Meta:
        model = Issue
        fields = (
            'issue_id', 'client_id', 'issue','community_id', 'description', 'solved'
        )
        depth = 1


class ThreadSerializer(serializers.ModelSerializer):
    thread_id = serializers.CharField(
        source='core_engine_community_app.thread', default=None
    )

    class Meta:
        model = Thread
        fields = (
            'thread_id', 'issue'
        )
        depth = 1