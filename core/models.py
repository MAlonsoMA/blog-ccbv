from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image

# MODELO CATEGORÍA
class Category (models.Model):
	name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
	active = models.BooleanField(default=True, verbose_name='Activo')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
	updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

	class Meta:
		verbose_name = 'Categoría'
		verbose_name_plural = 'Categorías'
		ordering = ['name']

	def __str__(self):
		return self.name

# MODELO DE ETIQUETAS
class Tag (models.Model):
	name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
	active = models.BooleanField(default=True, verbose_name='Activo')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
	updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

	class Meta:
		verbose_name = 'Etiqueta'
		verbose_name_plural = 'Etiquetas'
		ordering = ['name']

	def __str__(self):
		return self.name

# MODELO DE AUTOR = USUARIOS REGISTRADOS EN LA APLICACION => importando la tabla de usuarios

# MODELO DE LOS POSTS
def profile_picture_path(instance, filename):
    # Generar un nombre aleatorio usando la libreria uuid
    #random_filename = str(uuid.uuid4())
    # Recupero la extensión del archivo de imagen
    #extension = os.path.splitext(filename)[1]
    # Devuelvo la ruta completa final del archivo
    return 'posts/{}/{}'.format(instance.title, filename)

class Post(models.Model):
	title = models.CharField(max_length=250, verbose_name='Título')
	excerpt = models.TextField(verbose_name='Entradilla')
	content = RichTextField(verbose_name='Contenido')
	image = models.ImageField(default='default.jpg',upload_to=profile_picture_path, verbose_name='Imagen')
	published = models.BooleanField(default=False, verbose_name='Publicado')
	# Campos con relaciones
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='get_posts', verbose_name='Categoría')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_posts', verbose_name='Autor')
	tags = models.ManyToManyField(Tag, verbose_name='Etiquetas')
	likes = models.ManyToManyField(User, related_name='blog_posts', verbose_name='Me Gusta')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
	updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

	def save(self, *args, **kwargs):
			# Verificar que la imagen que estoy subiendo es diferente a la predeterminada
			if self.pk and self.image.name != 'default.jpg':
				old_profile = Post.objects.get(pk=self.pk)
				default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')

				if old_profile.image.path != self.image.path and old_profile.image.path != default_image_path:
					# Voy a eliminar la imagen anterior si es distinta de la actual y distinta de default.jpg
					default_storage.delete(old_profile.image.path)
			super(Post, self).save(*args, **kwargs)

			# Todo el codigo para recortar y redimensionar la imagen
			if self.image and os.path.exists(self.image.path):
				# Redimensionar la imagen antes de guardarla
				with Image.open(self.image.path) as img:
					ancho, alto = img.size

					if ancho > alto:
						# La imagen es mas ancha que alta
						nuevo_alto = 540
						#nuevo_ancho = int((ancho/alto) * nuevo_alto)
						nuevo_ancho = 850
						img = img.resize((nuevo_ancho, nuevo_alto))
						img.save(self.image.path)
					elif alto > ancho:
						# La imagen es mas alta que ancha
						nuevo_ancho = 540
						#nuevo_alto = int((alto/ancho) * nuevo_ancho )
						nuevo_alto = 850
						img = img.resize((nuevo_ancho, nuevo_alto))
						img.save(self.image.path)
					else:
						# La imagen es cuadrada
						img=img.resize((540,540))
						img.save(self.image.path)

				# El recorte de la imagen final
				with Image.open(self.image.path) as img:
					""" ancho, alto = img.size

						if ancho > alto:
						left = (ancho - alto) / 2
						top = 0
						right = (ancho + alto) / 2
						bottom = alto
					else:
						left = 0
						top = (alto - ancho) / 2
						right = ancho
						bottom = (alto + ancho) / 2

					img = img.crop((left, top, right, bottom)) """
					#comprimimos la imagen, 1-95, 1 minima calidad, 95 maxima
					calidad=60
					img.save(self.image.path,optimize=True,quality=calidad)


	def total_likes(self):
		return self.likes.count()

	class Meta:
		verbose_name = 'Publicación'
		verbose_name_plural = 'Publicaciones'
		ordering = ['-created']

	def __str__(self):
		return self.title

##########################################################

# MODELO ABOUT
class About(models.Model):
	description = models.CharField(max_length=350, verbose_name='Descripción')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
	updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

	class Meta:
		verbose_name = 'Acerca de'
		verbose_name_plural = 'Acerca de Nosotros'
		ordering = ['-created']

	def __str__(self):
		return self.description


# MODELO LINK = REDES SOCIALES
class Link(models.Model):
	key = models.CharField(max_length=100, verbose_name='Key Link')
	name = models.CharField(max_length=120, verbose_name='Red Social')
	url = models.URLField(max_length=350, blank=True, null=True, verbose_name='Enlace')
	icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='Icono')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
	updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

	class Meta:
		verbose_name = 'Red Social'
		verbose_name_plural = 'Redes Sociales'
		ordering = ['name']

	def __str__(self):
		return self.name
