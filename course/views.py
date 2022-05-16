from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.forms import ValidationError
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db import IntegrityError
from rest_framework import status

from course.serializers import CourseSerializer, PatchCourseSerializer, RegisterInstructorSerializer, RegisterStudentSerializer
from course.permissions import IsAdmin
from course.models import Course
from user.models import User


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request: Request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            create_course = Course.objects.create(**serializer.validated_data)

            course = CourseSerializer(create_course)
            return Response(
                course.data,
                status.HTTP_201_CREATED
            )

        except IntegrityError as e:
            return Response(
                {"message": "Name already exists"},
                status.HTTP_409_CONFLICT
            )

    def get(self, request: Request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

class CourseUuidView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request, course_uuid: str):
        try:
            course = Course.objects.filter(pk=course_uuid).first()
            serializer = CourseSerializer(course)

            return Response(
                serializer.data,
                status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                {"message": "Course does not exist"},
                status.HTTP_404_NOT_FOUND
            )

    def patch(self, request: Request, course_uuid: str):
        serializer = PatchCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            course_to_update = Course.objects.filter(pk=course_uuid)
            course_to_update.update(**serializer.validated_data)
            course = Course.objects.filter(pk=course_uuid).first()
            course_updated = CourseSerializer(course)

            return Response(
                course_updated.data,
                status.HTTP_200_OK
            )

        except IntegrityError as e:
            return Response(
                {"message": "Course name already exists"},
                status.HTTP_409_CONFLICT
            )

        except ValidationError as e:
            return Response(
                {"message": "Course does not exist"},
                status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request: Request, course_uuid: str):
        course = Course.objects.filter(pk=course_uuid).first()

        if not course:
            return Response(
                {"message": "Course does not exist"},
                status.HTTP_404_NOT_FOUND
            )
        course.delete()

        return Response(
            "",
            status.HTTP_204_NO_CONTENT
        )
    

@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def register_instructor(request: Request, course_uuid: str):
    serializer = RegisterInstructorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        course_to_update = Course.objects.filter(pk=course_uuid)
        instructor = User.objects.filter(
            pk=request.data["instructor_id"]).first()

        if not instructor.is_admin:
            return Response(
                {"message": "Instructor id does not belong to an admin"},
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        course_to_update.update(**serializer.validated_data)
        course = Course.objects.filter(pk=course_uuid).first()
        course_updated = CourseSerializer(course)
        course_updated = course_updated.data

        return Response(
            course_updated,
            status.HTTP_200_OK
        )

    except ValidationError as e:
        instructor = e.args[2]["value"]

        if instructor == request.data["instructor_id"]:
            return Response(
                {"message": "Invalid instructor_id"},
                status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Course does not exist"},
            status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def register_student(request: Request, course_uuid: str):
    serializer = RegisterStudentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        course_to_update = Course.objects.filter(pk=course_uuid).first()
        students = [
            User.objects.filter(pk=student_uuid).first()
            for student_uuid
            in serializer.validated_data["students_id"]
        ]

        if None in students:
            return Response(
                {"message": "Invalid students_id list"},
                status.HTTP_404_NOT_FOUND
            )

        if True in [item.is_admin for item in students]:
            return Response(
                {"message": "Some student id belongs to an Instructor"},
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        course_to_update.students.set(serializer.validated_data["students_id"])
        course = Course.objects.filter(pk=course_uuid).first()
        course_updated = CourseSerializer(course)
        course_updated = course_updated.data

        return Response(
            course_updated,
            status.HTTP_200_OK
        )

    except ValidationError as e:

        return Response(
            {"message": "Course does not exist"},
            status.HTTP_404_NOT_FOUND
        )