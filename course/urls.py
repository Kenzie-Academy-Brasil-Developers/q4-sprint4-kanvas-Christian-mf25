from django.urls import path

from course.views import CourseView, register_instructor, register_student, update_course

urlpatterns = [
	path("courses/", CourseView.as_view()),
	path("courses/<course_uuid>/", update_course),
	path("courses/<course_uuid>/registrations/instructor/", register_instructor),
	path("courses/<course_uuid>/registrations/students/", register_student)
]
