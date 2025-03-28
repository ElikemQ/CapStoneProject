from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import status
from serializers import RegisterSerializer, LoginSerializer, TokenSerializer
from rest_framework.authtoken.models import Token

# Create your views here.

# view to register user
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': RegisterSerializer(user).data, 'token' : TokenSerializer(token).data}, status=status.HTTP_400_BAD_REQUEST)


#view to login user
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': RegisterSerializer(user).data,
                             'token': TokenSerializer(token).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Credentials Invalid'}, status=status.HTTP_400_BAD_REQUEST)


# view for tokenretrieval 
class TokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.headers.get('Authorization')
        if token:
            try:
                token_obj = Token.objects.get(key=token)
                return Response({'token': token_obj.key}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'detail' : 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail' : 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)
    