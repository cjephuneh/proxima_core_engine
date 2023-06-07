import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from core_engine_tenant_users_app.models import (
    User, Employee, Client, Admin
)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    user_type = serializers.CharField(max_length=255, read_only=True)
 
    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
 
        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)
        #user_type = User(user_type=user.user_type)

 
        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        
        try:
            userObj = Admin.objects.get(email=user.email)
            user_type = Admin.objects.filter(user_type="Admin")

            

        except Admin.DoesNotExist:
            userObj = None

        try:
            if userObj is None:
                userObj = Employee.objects.get(email=user.email)
                user_type = Employee.objects.filter(user_type="Employee")
               
                

        except Employee.DoesNotExist:
            userObj = None
        
        try:
            if userObj is None:
                userObj = Client.objects.get(email=user.email)
                user_type = Client.objects.filter(user_type="Client")
               

        except Client.DoesNotExist:
            userObj = None

 
        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
 
        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        print(user_type)
        #user_type = str(user_type)
        return {
            'email': user.email,
            'token': user.token,
            'user_type': user_type
        }

class CheckTokenSerializer(serializers.Serializer):
    uidb64_regex = r"[0-9A-Za-z_\-]+"
    token_regex = r"[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}"
    uidb64 = serializers.RegexField(uidb64_regex)
    token = serializers.RegexField(token_regex)
    error_message = {"__all__": ("Invalid password reset token")}

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    retype_password = serializers.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_old_password(self, pwd):
        if not check_password(pwd, self.context.get("user").password):
            raise serializers.ValidationError("old password entered is incorrect.")
        return pwd

    def validate(self, data):
        if len(data.get("new_password")) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long!"
            )
        if data.get("new_password") == data.get("old_password"):
            raise serializers.ValidationError(
                "New_password and old password should not be the same"
            )
        if data.get("new_password") != data.get("retype_password"):
            raise serializers.ValidationError(
                "New_password and Retype_password did not match."
            )
        return data

class ResetPasswordSerailizer(CheckTokenSerializer):
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, data):
        self.user = self.get_user(data.get("uid"))
        if not self.user:
            raise serializers.ValidationError(self.error_message)
        is_valid_token = default_token_generator.check_token(
            self.user, data.get("token")
        )
        if not is_valid_token:
            raise serializers.ValidationError(self.error_message)
        new_password2 = data.get("new_password2")
        new_password1 = data.get("new_password1")
        if new_password1 != new_password2:
            raise serializers.ValidationError("The two password fields didn't match.")
        return new_password2

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email__iexact=email).last()
        if not user:
            raise serializers.ValidationError(
                "You don't have an account. Please create one."
            )
        return data
    
