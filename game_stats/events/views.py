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
    If multiple results have the same run_id and max_node, return the first or last.
    """
    # Step 1: Get the highest max_node for each run_id
    leaderboard_max_nodes = (
        Event.objects
        .exclude(max_node__isnull=True)  # Only include events where max_node is recorded
        .values('run_id')
        .annotate(max_node=Max('max_node'))  # Get the highest max_node for each run_id
    )

    # Step 2: Filter the original Event queryset by both run_id and max_node
    # Ensure that for each run_id/max_node pair, we return only the first or last event
    leaderboard_data = []
    for entry in leaderboard_max_nodes:
        # Get the first or last event by ordering on the timestamp or another unique field
        event = (
            Event.objects
            .filter(run_id=entry['run_id'], max_node=entry['max_node'])
            .order_by('timestamp')  # Or use '-timestamp' to get the latest, or any other field like 'id'
            .first()  # Use .last() if you prefer to get the last one
        )

        if event:
            leaderboard_data.append({
                'player': event.player,
                'run_id': event.run_id,
                'class_name': event.class_name,
                'patron': event.patron,
                'max_node': event.max_node,
                'timestamp': event.timestamp,  # Include any additional fields you need
            })

    return Response(leaderboard_data, status=status.HTTP_200_OK)

