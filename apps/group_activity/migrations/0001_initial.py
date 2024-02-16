# Generated by Django 5.0.2 on 2024-02-16 16:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MemberAuthentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_auth', models.BooleanField(default=False)),
                ('content', models.CharField(max_length=100, verbose_name='내용')),
                ('image', models.ImageField(blank=True, null=True, upload_to='authentication_images/', verbose_name='사진')),
                ('is_completed', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivityInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_left', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('authentication_count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
