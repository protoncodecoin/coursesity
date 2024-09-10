# Generated by Django 5.0.7 on 2024-09-09 22:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_image'),
        ('quiz', '0004_quiz_pass_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='module',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_module', to='courses.module'),
            preserve_default=False,
        ),
    ]
