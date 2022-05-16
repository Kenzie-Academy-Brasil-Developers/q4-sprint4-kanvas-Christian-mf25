from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from address.serializers import AddressSerializer
from user.serializers import UserSerializer
from address.models import Address
from user.models import User

class AddressView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_address = Address.objects.get_or_create(**serializer.validated_data)
        request.user.address = create_address[0]
        request.user.save()

        users_list = User.objects.filter(address=create_address[0].uuid)

        users = [UserSerializer(user).data for user in users_list]

        data = request.data
        data["users"] = users

        return Response(
			data,
			status.HTTP_200_OK
		)