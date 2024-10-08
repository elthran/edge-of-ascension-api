# Generated by Django 5.1.1 on 2024-10-07 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("new_run", "New Game Starts"),
                            ("boss_kill", "Boss Killed"),
                            ("game_over", "Player Dies"),
                        ],
                        max_length=50,
                    ),
                ),
                ("run_id", models.CharField(max_length=100)),
                ("player", models.CharField(max_length=100)),
                ("patron", models.CharField(blank=True, max_length=100, null=True)),
                ("class_name", models.CharField(blank=True, max_length=100, null=True)),
                ("boss_type", models.CharField(blank=True, max_length=100, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
