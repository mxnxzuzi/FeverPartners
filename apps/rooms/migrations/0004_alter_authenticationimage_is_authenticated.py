# Generated by Django 5.0.1 on 2024-01-31 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0003_authenticationimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authenticationimage",
            name="is_authenticated",
            field=models.BooleanField(default=False, verbose_name="인증여부"),
        ),
    ]
