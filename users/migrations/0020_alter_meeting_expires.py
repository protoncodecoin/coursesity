# Generated by Django 5.0.7 on 2024-10-10 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_meeting_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 13, 14, 34, 20, 590266, tzinfo=datetime.timezone.utc)),
        ),
    ]
