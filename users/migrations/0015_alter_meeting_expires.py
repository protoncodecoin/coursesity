# Generated by Django 5.0.7 on 2024-10-07 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_meeting_sch_date_meeting_sch_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 10, 19, 26, 26, 610744, tzinfo=datetime.timezone.utc)),
        ),
    ]
