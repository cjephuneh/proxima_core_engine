import logging
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from core_engine_auth_app.serializers import UserLoginSerializer
from rest_framework.permissions import AllowAny

class LoginAPIView(APIView):

    """
    Enable a user to sign in and issue them with a user token
    """
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)