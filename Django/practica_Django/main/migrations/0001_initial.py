# Generated by Django 3.0.3 on 2020-05-11 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Bodega')),
            ],
        ),
        migrations.CreateModel(
            name='Denominacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Denominación')),
            ],
        ),
        migrations.CreateModel(
            name='Uva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Uva')),
            ],
        ),
        migrations.CreateModel(
            name='Vino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('puntuacion', models.FloatField(verbose_name='Puntuacion')),
                ('bodega', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Bodega')),
                ('denominacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Denominacion')),
                ('uva', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Uva')),
            ],
        ),
    ]
