from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .models import Task
from .serializers import TaskSerializer


class TaskListCreate(APIView):

    def get(self, request):
        # Auto-delete tasks older than 24h
        cutoff = timezone.now() - timedelta(hours=24)
        Task.objects.filter(created_at__lt=cutoff).delete()

        # Show all tasks created within last 24 hours
        tasks = Task.objects.filter(created_at__gte=cutoff)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # created_at stored
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()               # Frontend vaporization delete
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def analytics(request):
    cutoff = timezone.now() - timedelta(hours=24)

    # Auto-delete old tasks
    Task.objects.filter(created_at__lt=cutoff).delete()

    # Count active tasks created within 24h
    qs = (Task.objects
            .filter(created_at__gte=cutoff)
            .values('category')
            .annotate(total=Count('id')))

    base = {'do': 0, 'schedule': 0, 'delegate': 0, 'eliminate': 0}
    for row in qs:
        base[row['category']] = row['total']

    return Response(base)

