# Generated by Django 3.0.14 on 2022-08-28 09:54

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0004_auto_20220827_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.City', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.Language', verbose_name='Язык программирования'),
        ),
    ]
