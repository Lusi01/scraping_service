# Generated by Django 3.0.14 on 2022-08-27 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.City', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.Language', verbose_name='Язык программирования'),
        ),
    ]
