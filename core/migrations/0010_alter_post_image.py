# Generated by Django 4.2.8 on 2024-06-18 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_about_content_about_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='media/about/', verbose_name='Imagen'),
        ),
    ]
