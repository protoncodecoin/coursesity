# Generated by Django 5.0.7 on 2024-09-11 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_quiz_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='module',
        ),
    ]
