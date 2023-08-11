from django.urls import path
from authentication.views import Auth

urlpatterns = [

    path("<uuid:id>/", Auth.as_view())
]