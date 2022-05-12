from django.urls import path

from user.views import LoginView, UserView


urlpatterns = [
	path("accounts/", UserView.as_view()),
	path("login/", LoginView.as_view()),
]