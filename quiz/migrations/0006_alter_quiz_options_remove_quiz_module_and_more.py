# Generated by Django 5.0.7 on 2024-09-09 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_image'),
        ('quiz', '0005_quiz_module'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='module',
        ),
        migrations.AddField(
            model_name='question',
            name='module',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_module', to='courses.module'),
            preserve_default=False,
        ),
    ]
