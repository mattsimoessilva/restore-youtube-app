# Generated by Django 4.2.5 on 2023-10-09 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meu_aplicativo', '0004_remove_channel_background_image_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='description',
        ),
    ]
