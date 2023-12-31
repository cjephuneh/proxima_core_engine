import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core_engine_community_app.models import Community
from core_engine_community_app.serializers import (
    CommunitySerializer, JoinCommunitySerializer, LeaveCommunitySerializer, ClientSerializer
)
from core_engine_community_app.utils import save_tenant_community
from core_engine_utils_app.views import get_filter_from_params

from django.db.models import Prefetch

from core_engine_tenant_users_app.models import (
    Client
)


log = logging.getLogger(__name__)


# class CommunityView(APIView):
#     """
#     Courses API View
#     """

#     def get(self, request, format=None):
#         """
#         GET
#         Retrieve courses matching query.

#         Params:
#         community_id
#         tenant_id
#         """
#         # Validate params args
#         params = request.query_params
#         allowed_params = {
#             'community_id': 'community_id',
#             'tenant_id': 'tenant_id'
#         }
#         filters = get_filter_from_params(params, allowed_params)

#         community_query = Community.objects.select_related('tenant_id').filter(**filters)
#         community_set = CommunitySerializer(community_query, many=True)
#         return Response(community_set.data, status=200)
class CommunityView(APIView):
    """
    Courses API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve courses matching query.

        Params:
        community_id
        tenant_id
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'community_id': 'community_id',
            'tenant_id': 'tenant_id'
        }
        filters = get_filter_from_params(params, allowed_params)

        community_query = Community.objects.prefetch_related('tenant_id').filter(**filters)

        # Include member details using prefetch_related
        # community_query = community_query.prefetch_related(
        #     Prefetch('members', queryset=Client.objects.all())
        # )

        community_set = CommunitySerializer(community_query, many=True)
        return Response(community_set.data, status=200)


class JoinCommunityView(APIView):

    serializer_class = JoinCommunitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Get the users email to be able to send activation token

        response = { 'error': False, 'data': serializer.data }
            
        return Response(response, status=status.HTTP_201_CREATED)
        
        
class LeaveCommunityView(APIView):
    serializer_class = LeaveCommunitySerializer

    def post(self, request):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Get the users email to be able to send activation token

            # This logic only applies if the client exists in the community
            # Otherwise, a 401 bad request with an error message is returned from the serializer
            response = { 'error': False, 'data': serializer.data }
            
            return Response(response, status=status.HTTP_201_CREATED)
    
class FavoriteCommunitiesView(APIView):
    def get(self, request, *args, **kwargs):
        client_id = request.query_params.get('client_id')

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=400)

        favorites = client.favorites.all()
        serializer = CommunitySerializer(favorites, many=True)

        return Response(serializer.data, status=200)
    
    # def post(self, request, *args, **kwargs):
    #     client_id = request.data.get('client_id')
    #     community_id = request.data.get('community_id')

    #     try:
    #         client = Client.objects.get(id=client_id)
    #     except Client.DoesNotExist:
    #         return Response({'error': 'Client not found'}, status=400)

    #     client.favorites.add(community_id)
    #     serializer = ClientSerializer(client)
    #     return Response(serializer.data, status=200) 

    # handle adding and removing from favorites list
    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client_id')
        community_id = request.data.get('community_id')

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_400_BAD_REQUEST)

        existing_favorites = client.favorites.filter(community_id=community_id)
        if existing_favorites.exists():
            client.favorites.remove(community_id)
            client.save()
            return Response({'message': 'Community removed from favorites'}, status=status.HTTP_200_OK)

        try:
            client.favorites.add(community_id)
            client.save()
        except Exception as e:
            return Response({'error': 'Failed to add/remove community from favorites'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Community added to favorites'}, status=status.HTTP_200_OK)



