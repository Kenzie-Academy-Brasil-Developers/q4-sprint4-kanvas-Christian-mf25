from rest_framework import serializers

class UserSerializer(serializers.Serializer):
	uuid = serializers.CharField(read_only=True)
	is_admin = serializers.BooleanField(required=False)
	email = serializers.EmailField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	username = serializers.CharField()
	password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
	email = serializers.CharField()
	password = serializers.CharField()