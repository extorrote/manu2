# Generated by Django 5.1.4 on 2025-01-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuelapp', '0005_remove_condo_youtube_video_condo_video_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condo',
            name='video',
        ),
        migrations.AddField(
            model_name='condo',
            name='youtube_iframe',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
