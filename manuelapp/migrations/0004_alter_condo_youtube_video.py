# Generated by Django 5.1.4 on 2025-01-25 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuelapp', '0003_rename_video_condo_youtube_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condo',
            name='youtube_video',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
