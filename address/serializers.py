from rest_framework import serializers

from user.serializers import UserSerializer

class AddressSerializer(serializers.Serializer):
	uuid = serializers.CharField(read_only=True)
	street = serializers.CharField()
	house_number = serializers.IntegerField()
	city = serializers.CharField()
	state = serializers.CharField()
	zip_code = serializers.CharField()
	country = serializers.CharField()
	users = UserSerializer(required=False, many=True)


class UserAddressSerializer(serializers.Serializer):
	address = AddressSerializer()