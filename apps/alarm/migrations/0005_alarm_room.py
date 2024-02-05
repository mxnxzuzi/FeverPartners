# Generated by Django 5.0.1 on 2024-02-05 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0004_alter_alarm_alarm_from'),
        ('rooms', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='rooms.room'),
        ),
    ]
