from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_type', 'game_version', 'run_id', 'player', 'patron', 'class_name', 'boss_type',
                  'max_node', 'timestamp']
