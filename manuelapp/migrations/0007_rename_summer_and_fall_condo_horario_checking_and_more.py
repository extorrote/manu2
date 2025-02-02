# Generated by Django 5.1.4 on 2025-01-28 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuelapp', '0006_remove_condo_video_condo_youtube_iframe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='condo',
            old_name='summer_and_fall',
            new_name='horario_checking',
        ),
        migrations.RenameField(
            model_name='condo',
            old_name='winter_and_spring',
            new_name='horario_checkout',
        ),
        migrations.AddField(
            model_name='condo',
            name='extra_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='condo',
            name='on_site_gym',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='condo',
            name='swimming_pool',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
