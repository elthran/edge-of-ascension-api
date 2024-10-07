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
    leaderboard_data = (
        Event.objects.filter(event_type='game_over')
        .exclude(max_node__isnull=True)  # Only include events where max_node is recorded
        .values('player', 'class_name', 'max_node')
        .order_by('-max_node')[:10]
    )
    return Response(leaderboard_data, status=status.HTTP_200_OK)
