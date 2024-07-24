# Generated by Django 5.0.7 on 2024-07-24 22:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_students'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['id', 'slug'], name='courses_cou_id_758a8e_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['title'], name='courses_cou_title_6e78a2_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['created'], name='courses_cou_created_ec4f1c_idx'),
        ),
    ]
