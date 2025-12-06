

from django.urls import path
from .views import TaskListCreate, analytics

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskListCreate.as_view(), name='task-delete'),
    path('analytics/', analytics, name='analytics'),
]
