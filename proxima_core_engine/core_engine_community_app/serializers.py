import logging
from rest_framework import serializers

from core_engine_community_app.models import (
    Comment, Community, Issue, Thread
)
from core_engine_tenant_users_app.models import (
    Client
)
# Comment serializers

# Client serializer to serialize the likes data
class ClientLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    likes = ClientLikesSerializer(many=True)
    client = ClientLikesSerializer(many=False)
    class Meta:
        model = Comment
        fields = ('comment_id', 'thread', 'client', 'comment_description', 'likes', 'dislikes')
        # read_only_fields = fields

"""
Community serializers
"""
# Community serializers

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB',]  # Include the fields you want to serialize for members

class CommunitySerializer(serializers.ModelSerializer):
    # tenant_id = serializers.CharField(
    #     source='core_engine_tenant_management_app.tenant', default=None
    # )
    members = MemberSerializer(many=True)  # Use the MemberSerializer for the members field

    class Meta:
        model = Community
        fields = ('community_id', 'tenant_id', 'description', 'members')
        # read_only_fields = ('position',)

#Join a particular community
# class JoinCommunitySerializer(serializers.ModelSerializer):
#     """serializers that enable a user to join a particular comunity
#     ."""
#     # client = serializers.CharField(
#     #     source='core_engine_tenant_users_app.client', default=None
#     # )
#     class Meta:
#         model = Community
#         fields = ['community_id',  'client_id',]

 
#     # def create(self, validated_data):
#         # return Community.objects.add_client_to_community(**validated_data)

class JoinCommunitySerializer(serializers.Serializer):
    community_id = serializers.IntegerField()
    client_id = serializers.IntegerField()

    def create(self, validated_data):
        community_id = validated_data['community_id']
        client_id = validated_data['client_id']

        community_instance = Community.objects.get(community_id=community_id) # retrieve the community
        client_instance = Client.objects.get(id=client_id)  # retrieve the client

        # check if the client id already a memeber of the community
        if client_instance in community_instance.members.all():
            raise serializers.ValidationError({"error": "client is already a member of this community"})
        else:
            event = community_instance.add_client_to_community(client_instance)
            return event

# Leave a community
class LeaveCommunitySerializer(serializers.Serializer):
    community_id = serializers.IntegerField()
    client_id = serializers.IntegerField()

    def create(self, validated_data):
        community_id = validated_data['community_id']
        client_id = validated_data['client_id']

        community_instance = Community.objects.get(community_id=community_id)
        client_instance = Client.objects.get(id=client_id)

        if client_instance in community_instance.members.all():
            event = community_instance.remove_client_from_community(client_instance)
            return event
        else:
            raise serializers.ValidationError({ "error": "client does not exist in the community"})

    
# #Join a particular community
# class LeaveCommunitySerializer(serializers.ModelSerializer):
#     """serializers that enable a user to join a particular comunity
#     ."""
#     client = serializers.CharField(
#         source='core_engine_tenant_users_app.client', default=None
#     )
#     class Meta:
#         model = Community
#         fields = ['client',]

 
#     def create(self, validated_data):
#         return Community.objects.remove_client_from_community(**validated_data)
    

# class IssueSerializer(serializers.ModelSerializer):
#     # client_id = serializers.CharField(
#     #     source='core_engine_tenant_users_app.client', default=None
#     # )
#     # community_id = serializers.CharField(
#     #     source='core_engine_community_app.community', default=None
#     # )
#     class Meta:
#         model = Issue
#         fields = (
#             'issue_id', 'client_id', 'issue','community_id', 'description', 'solved'
#         )
#         depth = 1
class IssueSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField()
    community_id = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('issue_id', 'issue', 'description', 'solved', 'client_id', 'community_id',)

    #  customize the serialization of the client_id field.
    def get_client_id(self, issue):
        # Customize the serialization of the client_id field
        client = issue.client_id
        return {'id': client.id, 'username': client.username, 'email': client.email, 'first_name': client.first_name, 'last_name': client.last_name}

    #  customize the serialization of the community_id field.
    def get_community_id(self, issue):
        # Customize the serialization of the community_id field
        community = issue.community_id
        return {'community_id': community.community_id, 'community_name': community.community_name}

    # limit the returned data 
    # customize the serialization by overriding the to_representation method
    def to_representation(self, instance):
        # Override the to_representation method to modify the serialized data
        data = super().to_representation(instance)
        # Customize the data dictionary as per your requirements
        # Remove any sensitive fields or include additional fields
        # data.pop('client_id')  # Remove the client_id field from the data dictionary
        return data


class ThreadSerializer(serializers.ModelSerializer):
    # thread_id = serializers.CharField(
    #     source='core_engine_community_app.thread', default=None
    # )

    class Meta:
        model = Thread
        fields = (
            'thread_id', 'issue'
        )
        depth = 1