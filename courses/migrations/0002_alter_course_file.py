# Generated by Django 4.2.5 on 2023-09-06 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='file',
            field=models.FileField(upload_to='courses_videos/'),
        ),
    ]