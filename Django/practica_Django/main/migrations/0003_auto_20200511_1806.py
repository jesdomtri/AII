# Generated by Django 3.0.3 on 2020-05-11 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200511_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vino',
            name='precio',
            field=models.FloatField(verbose_name='Precio'),
        ),
    ]
