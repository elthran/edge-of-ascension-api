# Generated by Django 5.1.1 on 2024-10-07 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="max_node",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]