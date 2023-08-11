from django.urls import path
from user.views import UserView

urlpatterns = [
    path("add/", UserView.as_view()),
    path("list/", UserView.as_view()),
]