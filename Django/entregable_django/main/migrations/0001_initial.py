# Generated by Django 3.0.3 on 2020-05-04 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Autor')),
            ],
        ),
        migrations.CreateModel(
            name='Fuente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Fuente')),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(verbose_name='Título')),
                ('fecha', models.DateField(verbose_name='Fecha y hora')),
                ('contenido', models.TextField(verbose_name='Contenido')),
                ('num_comentarios', models.IntegerField(verbose_name='Número de comentarios')),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Autor')),
                ('fuente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Fuente')),
            ],
        ),
    ]
