# events/models.py
from django.db import models


class Event(models.Model):
    EVENT_CHOICES = [
        ('new_run', 'New Game Starts'),
        ('boss_kill', 'Boss Killed'),
        ('game_over', 'Player Dies'),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    run_id = models.CharField(max_length=100)
    player = models.CharField(max_length=100)
    patron = models.CharField(max_length=100, null=True, blank=True)
    class_name = models.CharField(max_length=100, null=True, blank=True)
    boss_type = models.CharField(max_length=100, null=True, blank=True)  # Only for boss_kill events
    max_node = models.IntegerField(null=True, blank=True)  # Only for game_over events

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.run_id} - {self.player}"
