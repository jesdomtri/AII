# Generated by Django 3.0.3 on 2020-05-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vino',
            name='precio',
            field=models.TextField(verbose_name='Precio'),
        ),
    ]
