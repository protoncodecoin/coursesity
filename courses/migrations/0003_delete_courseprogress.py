# Generated by Django 5.0.7 on 2024-10-07 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_trigram_ext'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseProgress',
        ),
    ]
