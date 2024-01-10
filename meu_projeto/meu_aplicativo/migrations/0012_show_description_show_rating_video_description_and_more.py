# Generated by Django 4.2.5 on 2024-01-10 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_aplicativo', '0011_show_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='description',
            field=models.CharField(default='Explore o universo das religiões antigas com o historiador Thomas Rowsell. Esta série documental apresenta análises profundas, abordando a arqueologia, sociologia e genética de populações ancestrais. Viaje pelo mundo, encontre guerreiros corajosos, magos misteriosos, paisagens milenares, e conheça a diversidade da espécie humana.', max_length=340),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='rating',
            field=models.IntegerField(default=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.CharField(default='Explore o universo das religiões antigas com o historiador Thomas Rowsell. Esta série documental apresenta análises profundas, abordando a arqueologia, sociologia e genética de populações ancestrais. Viaje pelo mundo, encontre guerreiros corajosos, magos misteriosos, paisagens milenares, e conheça a diversidade da espécie humana.', max_length=340),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='rating',
            field=models.IntegerField(default=75),
            preserve_default=False,
        ),
    ]