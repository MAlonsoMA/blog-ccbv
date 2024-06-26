# Generated by Django 4.1.1 on 2024-05-02 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre localización')),
                ('address', models.CharField(max_length=250, verbose_name='Dirección')),
                ('lat', models.FloatField(verbose_name='Latitud')),
                ('lng', models.FloatField(verbose_name='Longitud')),
            ],
            options={
                'verbose_name': 'Localización',
                'verbose_name_plural': 'Localizaciones',
                'ordering': ['name'],
            },
        ),
    ]
