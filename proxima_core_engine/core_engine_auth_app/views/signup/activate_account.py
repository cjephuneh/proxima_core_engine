import json
from multiprocessing import context
from re import template

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_tenant_users_app.models import User
from core_engine_auth_app.serializers import ( PasswordChangeSerializer,ForgotPasswordSerializer
                            )
from core_engine_auth_app.tasks import (resend_activation_link_to_user,
                          )
from core_engine_auth_app.token_generator import account_activation_token

class ActivateUserView(View):
    template = "core_engine_auth_app/user_activation_status.html"
    # @swagger_auto_schema(
    #     tags=["Auth"],
    # )
    def get(self, request, uid, token, activation_key, format=None):
        user = User.objects.get(activation_key=activation_key)
        if user:
            if timezone.now() > user.key_expires:
                resend_activation_link_to_user.delay(
                    user.email,
                )
                context = {
                    "success": False,
                    "message": "Link expired. Please use the Activation link sent now to your mail.",
                }
                return render(request, self.template, context)
            else:
                try:
                    uid = force_str(urlsafe_base64_decode(uid))
                    user = User.objects.get(pk=uid)
                except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    user = None
                if user is not None and account_activation_token.check_token(
                    user, token
                ):
                    user.is_active = True
                    user.save()

                    context = {
                        "success": True,
                        "message": "Thank you for your email confirmation. Now you can login to your account.",
                    }
                    return render(request, self.template, context)

                context = {"success": False, "message": "In Valid Token."}
                return render(request, self.template, context)



class ResendActivationLinkView(APIView):

    def post(self, request, format=None):
        params = request.post_data
        user = get_object_or_404(User, email=params.get("email"))
        if user.is_active:
            return Response(
                {"error": False, "message": "Account is active. Please login"},
                status=status.HTTP_200_OK,
            )
        resend_activation_link_to_user.delay(
            user.email,
        )
        data = {
            "error": False,
            "message": "Please use the Activation link sent to your mail to activate account.",
        }
        return Response(data, status=status.HTTP_200_OK)

