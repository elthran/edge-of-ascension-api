# events/serializers.py
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_type', 'run_id', 'player', 'patron', 'class_name', 'boss_type', 'max_node', 'timestamp']
