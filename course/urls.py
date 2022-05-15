from django.urls import path

from course.views import CourseView, update_course

urlpatterns = [
	path("courses/", CourseView.as_view()),
	path("courses/<course_uuid>/", update_course)
]
