# Generated by Django 3.0.14 on 2022-08-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_auto_20220827_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название населенного пункта'),
        ),
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
