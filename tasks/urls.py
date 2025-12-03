
from rest_framework import routers
from django.urls import path
from .views import TaskViewSet, analytics

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('analytics/', analytics, name='analytics'),
]

urlpatterns += router.urls
