from rest_framework import serializers
from .models import (
    AdminProfile, EmployeeProfile, ClientProfile
)

from core_engine_tenant_users_app.models import (
    Admin, Employee, Client)

class AdminProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='admin.username')
    profile_photo  = serializers.SerializerMethodField()
    country  = serializers.CharField(allow_blank=True, required=False)
    county = serializers.CharField(allow_blank=True, required=False)
    city  = serializers.CharField(allow_blank=True, required=False)
    postal_code = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = AdminProfile
        fields = ('username','profile_photo', 'country', 'county', 'city',
        'postal_code', 'location' )
        read_only_fields = ('username',)

    def get_profile_photo(self, obj):
        if obj.profile_photo:
            return obj.profile_photo

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
    

class EmployeeProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='employee.username')
    profile_photo  = serializers.SerializerMethodField()
    country  = serializers.CharField(allow_blank=True, required=False)
    county = serializers.CharField(allow_blank=True, required=False)
    city  = serializers.CharField(allow_blank=True, required=False)
    postal_code = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = EmployeeProfile
        fields = ('username','profile_photo', 'country', 'county', 'city',
        'postal_code', 'location' )
        read_only_fields = ('username',)

    def get_profile_photo(self, obj):
        if obj.profile_photo:
            return obj.profile_photo

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
    

class ClientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='client.username')
    profile_photo  = serializers.SerializerMethodField()
    country  = serializers.CharField(allow_blank=True, required=False)
    county = serializers.CharField(allow_blank=True, required=False)
    city  = serializers.CharField(allow_blank=True, required=False)
    postal_code = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = ClientProfile
        fields = ('username','profile_photo', 'country', 'county', 'city',
        'postal_code', 'location' )
        read_only_fields = ('username',)

    def get_profile_photo(self, obj):
        if obj.profile_photo:
            return obj.profile_photo

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'

"""
Updating All profiles  - admin, employee, client
"""

# Admin

class AdminUserSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of user objects
    """
    password = serializers.CharField(
        max_length=128,
        min_length = 8,
        write_only = True
    )
    """
        We explicitly specify that the profile should be handled as a serializer and
        we do not want to expose the profile info so it is write only
    """

    profile = AdminProfile()
    profile_photo  = serializers.CharField(source='profile.profile_photo', read_only=True)
    country = serializers.CharField(source='profile.country', read_only=True)
    county = serializers.CharField(source='profile.county', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    postal_code = serializers.CharField(source='profile.postal_code', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)

    class Meta:
        model = Admin
        fields  = ['id', 'first_name', 'last_name','username', 'phonenumber', 'email', 'gender', 'DOB', 'password', 'token', 'profile',
        'profile_photo', 'country', 'county', 'city', 'postal_code', 'location']

        read_only_fields = ('token', )

    def update(self, instance, validated_data):
        """
        Performs an update on a user
        """
        #We need to remove password field from validated data before iterating over it

        password = validated_data.pop('password')

        #Like passwords we need to handle the profile data separately so we remove it
        #from the 'validated_data' dictionary

        profile_data = validated_data.pop('profile', {})
    

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            #Handling password
            instance.set_password(password)

        instance.save()


        #We are going to do the same thing as above but this time for the profile model
        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        #Save the instance like the profile
        instance.profile.save

        return instance
    
# Employee

class EmployeeUserSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of user objects
    """
    password = serializers.CharField(
        max_length=128,
        min_length = 8,
        write_only = True
    )
    """
        We explicitly specify that the profile should be handled as a serializer and
        we do not want to expose the profile info so it is write only
    """

    profile = EmployeeProfile()
    profile_photo  = serializers.CharField(source='profile.profile_photo', read_only=True)
    country = serializers.CharField(source='profile.country', read_only=True)
    county = serializers.CharField(source='profile.county', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    postal_code = serializers.CharField(source='profile.postal_code', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)

    class Meta:
        model = Employee
        fields  = ['id', 'first_name', 'last_name','username', 'phonenumber', 'email', 'gender', 'DOB', 'password', 'token', 'profile',
        'profile_photo', 'country', 'county', 'city', 'postal_code', 'location']

        read_only_fields = ('token', )

    def update(self, instance, validated_data):
        """
        Performs an update on a user
        """
        #We need to remove password field from validated data before iterating over it

        password = validated_data.pop('password')

        #Like passwords we need to handle the profile data separately so we remove it
        #from the 'validated_data' dictionary

        profile_data = validated_data.pop('profile', {})
    

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            #Handling password
            instance.set_password(password)

        instance.save()


        #We are going to do the same thing as above but this time for the profile model
        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        #Save the instance like the profile
        instance.profile.save

        return instance
    
# Client

class ClientUserSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of user objects
    """
    password = serializers.CharField(
        max_length=128,
        min_length = 8,
        write_only = True
    )
    """
        We explicitly specify that the profile should be handled as a serializer and
        we do not want to expose the profile info so it is write only
    """

    profile = ClientProfile()
    profile_photo  = serializers.CharField(source='profile.profile_photo', read_only=True)
    country = serializers.CharField(source='profile.country', read_only=True)
    county = serializers.CharField(source='profile.county', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    postal_code = serializers.CharField(source='profile.postal_code', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)

    class Meta:
        model = Client
        fields  = ['id', 'first_name', 'last_name','username', 'phonenumber', 'email', 'gender', 'DOB', 'password', 'token', 'profile',
        'profile_photo', 'country', 'county', 'city', 'postal_code', 'location']

        read_only_fields = ('token', )

    def update(self, instance, validated_data):
        """
        Performs an update on a user
        """
        #We need to remove password field from validated data before iterating over it

        password = validated_data.pop('password')

        #Like passwords we need to handle the profile data separately so we remove it
        #from the 'validated_data' dictionary

        profile_data = validated_data.pop('profile', {})
    

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            #Handling password
            instance.set_password(password)

        instance.save()


        #We are going to do the same thing as above but this time for the profile model
        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        #Save the instance like the profile
        instance.profile.save

        return instance