from django.shortcuts import render

# Create your views here.
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core_engine_tenant_users_app.serializers import ClientSerializer
from core_engine_auth_app.tasks import ( send_email_to_new_user )


class ClientAPIView(APIView):
    #Allow any user authenticated or not to hit this endpoint
    permission_classes = (AllowAny,)
    #renderer_classes = (DermatologistUserJSONRenderer,)
    serializer_class = ClientSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # user_obj = serializer.save()
            # Get the users email to be able to send activation token
            # user_email = user_obj.email
            # send_email_to_new_user.delay(
            #         user_email
            #     )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except:
            return Response(
                {
                    "error": True,
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
