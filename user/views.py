from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from user.serializers import LoginSerializer, UserSerializer
from user.models import User

class UserView(APIView):
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        found_user = User.objects.filter(
            email=serializer.validated_data["email"]
        ).exists()

        if found_user:
            return Response(
                {"message": "User already exists"}, status.HTTP_409_CONFLICT
            )

        user = User.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user: User = User.objects.filter(
            email=serializer.validated_data["email"]
        ).first()

        if not user or not check_password(serializer.validated_data["password"], user.password):
            return Response({
                "message": "Invalid password or e-mail address"}, status.HTTP_401_UNAUTHORIZED
            )
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key}, status.HTTP_200_OK
        )