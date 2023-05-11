from rest_framework import serializers, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from core_engine_users_profile_app.serializers import (
    EmployeeProfileSerializer, EmployeeUserSerializer )
from rest_framework.generics import RetrieveUpdateAPIView
from core_engine_users_profile_app.models import EmployeeProfile



class EmployeeProfileRetrieveAPIView(RetrieveAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    lookup_field = 'employee_id'

class EmployeeRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = EmployeeUserSerializer

   
    def retrieve(self, request, *args, **kwargs):
        #We want the serializer to Jsonify our user and send to client
        serializer = self.serializer_class(request.employee)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        employee_data = request.data.get('employee', {})

        serializer_data = {
            'first_name': employee_data.get('first_name', request.employee.first_name),
            'last_name': employee_data.get('last_name', request.employee.last_name),
            'username': employee_data.get('username', request.employee.username),
            'email': employee_data.get('email', request.employee.email),
            'phonenumber': employee_data.get('phonenumber', request.employee.phonenumber),
            'gender': employee_data.get('gender', request.employee.gender),
            'DOB': employee_data.get('DOB', request.employee.DOB),
            'profile': {
                'profile_photo': employee_data.get('profile_photo', request.employee.profile.profile_photo),
                'country': employee_data.get('country', request.employee.profile.country),
                'county': employee_data.get('county', request.employee.profile.county),
                'city': employee_data.get('city', request.employee.profile.city),
                'postal_code': employee_data.get('postal_code', request.employee.profile.postal_code),
                'location': employee_data.get('location', request.employee.profile.location)

            }
        }



        #serializer_data = request.data.get('employee', {})

        serializer = self.serializer_class(
            request.employee, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status = status.HTTP_200_OK)




    
    def perform_create(self, serializer):
        serializer.save(employee=self.request.employee)
