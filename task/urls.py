from django.urls import path
from task.views import TaskManager, TaskListManager, TaskOperationsManager

urlpatterns = [
    path("<uuid:id>/", TaskManager.as_view()),
    path("add/", TaskManager.as_view()),
    path("update/<uuid:id>/", TaskManager.as_view()),
    path("<uuid:id>/", TaskManager.as_view()),
    path("list/", TaskListManager.as_view()),
    path("assign/", TaskOperationsManager.as_view()),
]