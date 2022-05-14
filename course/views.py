from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
# from psycopg2 import IntegrityError
from rest_framework import status

from course.serializers import CourseSerializer, CreateCourseSerializer
from course.permissions import IsAdmin
from course.models import Course


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request: Request):
        serializer = CreateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            create_course= Course.objects.create(**serializer.validated_data)
            
            course = CourseSerializer(create_course)
            return Response(course.data, status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"message": "key name already exists"}, status.HTTP_409_CONFLICT)