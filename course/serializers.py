from rest_framework import serializers

from user.serializers import UserSerializer

class CourseSerializer(serializers.Serializer):
	uuid = serializers.CharField(read_only=True)
	name = serializers.CharField()
	demo_time = serializers.TimeField()
	created_at = serializers.DateTimeField(read_only=True)
	link_repo = serializers.CharField()
	instructor = UserSerializer(required=False)
	students = UserSerializer(required=False, many=True)

class PatchCourseSerializer(serializers.Serializer):
	name = serializers.CharField(required=False)
	demo_time = serializers.TimeField(required=False)
	link_repo = serializers.CharField(required=False)