from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (LoginSerializer, RegisterSerializer)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                response_data = {
                    'message': _('Welcome {}!'.format(user.first_name))
                }
                response = Response(response_data, status=status.HTTP_200_OK)
                response['Authorization'] = 'Token {}'.format(token.key)
                return response
            else:
                return Response({'error': _('Invalid email or password.')}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Check if the email is already registered
            if get_user_model().objects.filter(email=email).exists():
                return Response({'error': _('Email is already registered.')},
                                status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({'message': _('Successful Registration!')}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
