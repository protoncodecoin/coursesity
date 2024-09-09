# Generated by Django 5.0.7 on 2024-09-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default='users/default.jpg', upload_to='users/%Y/%m/%d'),
        ),
    ]
