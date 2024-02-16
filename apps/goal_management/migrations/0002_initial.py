# Generated by Django 5.0.2 on 2024-02-16 16:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goal_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='achievementreport',
            name='reacted_dislike',
            field=models.ManyToManyField(default=None, related_name='disliked_reports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievementreport',
            name='reacted_love',
            field=models.ManyToManyField(default=None, related_name='loved_reports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievementreport',
            name='reacted_respectful',
            field=models.ManyToManyField(default=None, related_name='respected_reports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='goal',
            name='activityTags',
            field=models.ManyToManyField(default=None, to='goal_management.activitytag'),
        ),
        migrations.AddField(
            model_name='goal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievementreport',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goal_management.goal'),
        ),
        migrations.AddField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goal_management.tag'),
        ),
        migrations.AddField(
            model_name='goal',
            name='tags',
            field=models.ManyToManyField(default=None, to='goal_management.tag'),
        ),
        migrations.AddField(
            model_name='userreport',
            name='report_target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='goal_management.achievementreport'),
        ),
        migrations.AddField(
            model_name='userreport',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to=settings.AUTH_USER_MODEL),
        ),
    ]
