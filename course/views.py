from django.forms import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db import IntegrityError
from rest_framework import status

from course.serializers import CourseSerializer, PatchCourseSerializer
from course.permissions import IsAdmin
from course.models import Course


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request: Request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            create_course= Course.objects.create(**serializer.validated_data)
            
            course = CourseSerializer(create_course)
            return Response(course.data, status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"message": "key name already exists"}, status.HTTP_409_CONFLICT)


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def update_course(request: Request, course_uuid: str):
    serializer = PatchCourseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        course_to_update = Course.objects.filter(pk=course_uuid)
        course_to_update.update(**serializer.validated_data)
        course = Course.objects.filter(pk=course_uuid).first()
        course_updated = CourseSerializer(course)

        return Response(course_updated.data, 201)

    except IntegrityError as e:
        return Response({"message": "Course name already exists"}, status.HTTP_409_CONFLICT)

    except ValidationError as err:
        return Response({"message": "Course does not exist"}, status.HTTP_404_NOT_FOUND)   