from django.urls import path

from course.views import CourseView

urlpatterns = [
	path("courses/", CourseView.as_view())
]
