from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    Serve a leaderboard showing the top 10 players with the highest 'max_node' for a specific game version.
    If multiple results have the same run_id and max_node, return the first or last.
    """

    # Step 1: Get the game_version from query parameters (optional)
    game_version = request.query_params.get('game_version', '000.000.011')

    # Step 2: Get the highest max_node for each run_id, and filter by game_version if provided
    leaderboard_max_nodes = Event.objects.exclude(max_node__isnull=True).filter(max_node__gte=3)

    if game_version:
        leaderboard_max_nodes = leaderboard_max_nodes.filter(game_version=game_version)

    leaderboard_max_nodes = (leaderboard_max_nodes.values('run_id').annotate(max_node=Max('max_node'))
    # Get the highest max_node for each run_id
    )

    # Step 3: Filter the original Event queryset by both run_id and max_node
    leaderboard_data = []
    for entry in leaderboard_max_nodes:
        # Get the first or last event by ordering on the timestamp or another unique field
        event = (Event.objects.filter(run_id=entry['run_id'], max_node=entry['max_node']))

        if game_version:
            event = event.filter(game_version=game_version)  # Apply version filter here as well

        event = event.order_by('timestamp').first()  # Use .last() if you prefer the last one

        if event:
            leaderboard_data.append({
                'game_version': event.game_version,
                'player': event.player,
                'run_id': event.run_id,
                'class_name': event.class_name,
                'patron': event.patron,
                'max_node': event.max_node,
                'timestamp': event.timestamp,  # Include any additional fields you need
            })

    return Response(leaderboard_data, status=status.HTTP_200_OK)
