# Generated by Django 5.0.1 on 2024-02-05 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0005_alarm_room'),
        ('group_management', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='group_management.room'),
        ),
    ]
