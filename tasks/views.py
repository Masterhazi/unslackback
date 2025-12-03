
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer


@api_view(['GET'])
def analytics(request):
    base = {'do': 0, 'schedule': 0, 'delegate': 0, 'eliminate': 0}
    qs = Task.objects.values('category').annotate(total=Count('id'))
    for row in qs:
        base[row['category']] = row['total']
    return Response(base)
