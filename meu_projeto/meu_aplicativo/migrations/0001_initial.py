# Generated by Django 4.2.5 on 2024-02-16 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('logo', models.URLField()),
                ('wallpaper', models.URLField(default='https://img.zcool.cn/community/03837b955deb1590000015995760355.jpg')),
                ('description', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('url', models.URLField()),
                ('thumbnail', models.URLField()),
                ('uploadedDate', models.CharField(max_length=50)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meu_aplicativo.channel')),
            ],
        ),
    ]
