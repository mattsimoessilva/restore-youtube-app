# Generated by Django 4.2.5 on 2024-02-20 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_aplicativo', '0009_batch_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='title',
            field=models.CharField(default='Study', max_length=100),
            preserve_default=False,
        ),
    ]
