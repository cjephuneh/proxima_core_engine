from rest_framework import serializers, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from core_engine_users_profile_app.serializers import (
    AdminProfileSerializer, AdminUserSerializer )
from rest_framework.generics import RetrieveUpdateAPIView
from core_engine_users_profile_app.models import AdminProfile



class AdminProfileRetrieveAPIView(RetrieveAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    lookup_field = 'admin_id'

class AdminRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = AdminUserSerializer

   
    def retrieve(self, request, *args, **kwargs):
        #We want the serializer to Jsonify our user and send to client
        serializer = self.serializer_class(request.admin)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        admin_data = request.data.get('admin', {})

        serializer_data = {
            'first_name': admin_data.get('first_name', request.admin.first_name),
            'last_name': admin_data.get('last_name', request.admin.last_name),
            'username': admin_data.get('username', request.admin.username),
            'email': admin_data.get('email', request.admin.email),
            'phonenumber': admin_data.get('phonenumber', request.admin.phonenumber),
            'gender': admin_data.get('gender', request.admin.gender),
            'DOB': admin_data.get('DOB', request.admin.DOB),
            'profile': {
                'profile_photo': admin_data.get('profile_photo', request.admin.profile.profile_photo),
                'country': admin_data.get('country', request.admin.profile.country),
                'county': admin_data.get('county', request.admin.profile.county),
                'city': admin_data.get('city', request.admin.profile.city),
                'postal_code': admin_data.get('postal_code', request.admin.profile.postal_code),
                'location': admin_data.get('location', request.admin.profile.location)

            }
        }



        #serializer_data = request.data.get('admin', {})

        serializer = self.serializer_class(
            request.admin, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)




    
    def perform_create(self, serializer):
        serializer.save(admin=self.request.admin)
