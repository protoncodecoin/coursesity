# Generated by Django 5.0.7 on 2024-09-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_remove_question_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(max_length=300, null=True),
        ),
    ]
