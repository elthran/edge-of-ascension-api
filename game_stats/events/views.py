# events/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from .models import Event
from .serializers import EventSerializer

@api_view(['POST'])
def record_event(request):
    """
    Handles recording events such as new game start, boss kill, and game over.
    """
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def leaderboard(request):
    """
    Serve a leaderboard showing the top 10 players with the highest 'max_node'.
    """
    # Get the highest max_node for each run_id
    leaderboard_data = (
        Event.objects
        .exclude(max_node__isnull=True)  # Only include events where max_node is recorded
        .values('run_id')  # Group by run_id
        .annotate(max_node=Max('max_node'))  # Get the highest max_node for each run_id
    )

    # Join back to the original query to get other fields like player, class_name
    leaderboard_data = (
        Event.objects
        .filter(run_id__in=[entry['run_id'] for entry in leaderboard_data])
        .values('player', 'run_id', 'class_name', 'patron', 'max_node')
        .order_by('-max_node')[:50]  # Order by max_node descending, and limit to top 10
    )

    return Response(leaderboard_data, status=status.HTTP_200_OK)
