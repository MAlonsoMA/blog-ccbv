from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre localización')
    address = models.CharField(max_length=250, verbose_name='Dirección')
    lat = models.FloatField(verbose_name='Latitud')
    lng = models.FloatField(verbose_name='Longitud')

    class Meta:
        verbose_name = 'Localización'
        verbose_name_plural = 'Localizaciones'
        ordering = ['name']

    def __str__(self):
        return self.name