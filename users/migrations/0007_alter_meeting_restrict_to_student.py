# Generated by Django 5.0.7 on 2024-09-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_meeting_restrict_to_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='restrict_to_student',
            field=models.BooleanField(default=True, help_text='allow only enrolled students in the meeting'),
        ),
    ]
