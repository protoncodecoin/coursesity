# Generated by Django 5.0.7 on 2024-09-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_description',
            field=models.TextField(blank=True),
        ),
    ]
