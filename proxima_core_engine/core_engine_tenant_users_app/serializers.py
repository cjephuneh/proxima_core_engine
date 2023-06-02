from rest_framework import serializers
from core_engine_tenant_users_app.models import (
Admin, AnonymousUser, Client, Employee
)

class AdminSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    # tenant_id  = serializers.IntegerField(source='core_engine_tenant_management_app.Tenant')
 
    class Meta:
        model = Admin
        fields = ['username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB', 'user_type','tenant_id', 'password', 'confirm_password','token' ]

 
    def create(self, validated_data):
        return Admin.objects.create_admin(**validated_data)


class ClientSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    # tenant_id  = serializers.UUIDField(source='core_engine_tenant_management_app.Tenant')

    class Meta:
        model = Client
        fields = ['id','username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB', 'user_type', 'password', 'confirm_password','token' ]

 
    def create(self, validated_data):
        return Client.objects.create_client(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    token = serializers.CharField(max_length=255, read_only=True)
    # tenant_id  = serializers.UUIDField(source='core_engine_tenant_management_app.Tenant')

 
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'first_name', 'last_name','phonenumber', 'gender','DOB', 'user_type','tenant_id', 'password', 'confirm_password','token' ]

 
    def create(self, validated_data):
        return Employee.objects.create_employee(**validated_data)


class AnonymousUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnonymousUser
        fields = '__all__'

 