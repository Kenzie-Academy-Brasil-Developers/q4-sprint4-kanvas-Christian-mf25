from django.urls import path

from course.views import CourseUuidView, CourseView, register_instructor, register_student

urlpatterns = [
	path("courses/", CourseView.as_view()),
	path("courses/<uuid>/", CourseUuidView.as_view()),
	path("courses/<uuid>/registrations/instructor/", register_instructor),
	path("courses/<uuid>/registrations/students/", register_student),
]