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
        cutoff = timezone.now() - timedelta(hours=24)
        Task.objects.filter(created_at__lt=cutoff).delete()

        tasks = Task.objects.filter(completed=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def analytics(request):
    # ⭐ Delete old tasks here too — analytics must match list
    cutoff = timezone.now() - timedelta(hours=24)
    Task.objects.filter(created_at__lt=cutoff).delete()

    # ⭐ Count only uncompleted tasks (active tasks)
    base = {'do': 0, 'schedule': 0, 'delegate': 0, 'eliminate': 0}
    qs = Task.objects.filter(completed=False).values('category').annotate(total=Count('id'))

    for row in qs:
        base[row['category']] = row['total']

    return Response(base)
