from django.urls import path

from course.views import CourseUuidView, CourseView, register_instructor, register_student

urlpatterns = [
	path("courses/", CourseView.as_view()),
	path("courses/<course_uuid>/", CourseUuidView.as_view()),
	path("courses/<course_uuid>/registrations/instructor/", register_instructor),
	path("courses/<course_uuid>/registrations/students/", register_student),
]