from rest_framework import serializers, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from core_engine_users_profile_app.serializers import (
    ClientProfileSerializer, ClientUserSerializer )
from rest_framework.generics import RetrieveUpdateAPIView
from core_engine_users_profile_app.models import ClientProfile



class ClientProfileRetrieveAPIView(RetrieveAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    lookup_field = 'client_id'

class ClientRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ClientUserSerializer

   
    def retrieve(self, request, *args, **kwargs):
        #We want the serializer to Jsonify our user and send to client
        serializer = self.serializer_class(request.client)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        client_data = request.data.get('client', {})

        serializer_data = {
            'first_name': client_data.get('first_name', request.client.first_name),
            'last_name': client_data.get('last_name', request.client.last_name),
            'username': client_data.get('username', request.client.username),
            'email': client_data.get('email', request.client.email),
            'phonenumber': client_data.get('phonenumber', request.client.phonenumber),
            'gender': client_data.get('gender', request.client.gender),
            'DOB': client_data.get('DOB', request.client.DOB),
            'profile': {
                'profile_photo': client_data.get('profile_photo', request.client.profile.profile_photo),
                'country': client_data.get('country', request.client.profile.country),
                'county': client_data.get('county', request.client.profile.county),
                'city': client_data.get('city', request.client.profile.city),
                'postal_code': client_data.get('postal_code', request.client.profile.postal_code),
                'location': client_data.get('location', request.client.profile.location)

            }
        }



        #serializer_data = request.data.get('client', {})

        serializer = self.serializer_class(
            request.client, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)




    
    def perform_create(self, serializer):
        serializer.save(client=self.request.client)
