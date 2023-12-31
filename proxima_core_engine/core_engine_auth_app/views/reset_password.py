from rest_framework import status
from rest_framework.views import APIView
from django.utils.encoding import force_str
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from core_engine_tenant_users_app.models import Client
from rest_framework.permissions import IsAuthenticated, AllowAny
from core_engine_auth_app.tasks import (
                           send_email_to_reset_password,
                          )
from core_engine_auth_app.serializers import ( PasswordChangeSerializer,ForgotPasswordSerializer
                            )

from core_engine_tenant_users_app.models import Client
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail

class ForgotPasswordView(APIView):
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        recipient_list = ['o.becks45@gmail.com', 'proximaagents@gmail.com']#request.data.get('recipient_list')

        send_mail(subject, message, 'administrator@proximaai.co', recipient_list)

        return Response({'success': 'Email sent successfully'})
    
class ChangePasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Get the client/user based on the provided email
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=404)

        # Set the new password for the client
        client.set_password(password)
        client.save()

        return Response({'success': 'Password changed successfully'})

# class ChangePasswordView(APIView):
#     ##authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (AllowAny,)

#     def post(self, request, format=None):
#         params = request.post_data
#         context = {"user": request.user}
#         serializer = PasswordChangeSerializer(data=params, context=context)
#         if serializer.is_valid():
#             user = request.user
#             user.set_password(params.get("new_password"))
#             user.save()
#             return Response(
#                 {"error": False, "message": "Password Changed Successfully"},
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             {"error": True, "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

# class ForgotPasswordView(APIView):

#     permission_classes = (AllowAny,)


#     def post(self, request, format=None):
#         params = request.post_data
#         serializer = ForgotPasswordSerializer(data=params)
#         if serializer.is_valid():
#             user = get_object_or_404(User, email=params.get("email"))
#             if not user.is_active:
#                 return Response(
#                     {"error": True, "errors": "Please activate account to proceed."},
#                     status=status.HTTP_406_NOT_ACCEPTABLE,
#                 )
#             send_email_to_reset_password.delay(user.email)
#             data = {
#                 "error": False,
#                 "message": "We have sent you an email. please reset password",
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         else:

#             error = serializer.errors.get("non_field_errors")

#             data = {"error": True, "errors": serializer.errors, "error_text": error[0]}
#             response_status = status.HTTP_400_BAD_REQUEST
#             return Response(data, status=response_status)

class ResetPasswordView(APIView):

    def post(self, request, uid, token, format=None):
        params = request.post_data
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user_obj = User.objects.get(pk=uid)
            if not user_obj.password:
                if not user_obj.is_active:
                    user_obj.is_active = True
                    user_obj.save()
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user_obj = None
        if user_obj is not None:
            password1 = params.get("new_password1")
            password2 = params.get("new_password2")
            if password1 != password2:
                return Response(
                    {"error": True, "errors": "The two password fields didn't match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user_obj.set_password(password1)
                user_obj.save()
                return Response(
                    {
                        "error": False,
                        "message": "Password Updated Successfully. Please login",
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response({"error": True, "errors": "Invalid Link"})



