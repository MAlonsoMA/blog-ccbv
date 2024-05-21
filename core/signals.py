import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post
import os

@receiver(post_delete, sender=Post)
def delete_imagen(sender, instance, **kwargs):

        if instance.image and instance.image.name != "default.jpg":
            image_path=instance.image.path
            image_dir=os.path.dirname(image_path)

            #eliminar la imagen
            if os.path.isfile(image_path):
                os.remove(image_path)

            #eliminar la carpeta si esta vacia
            if not os.listdir(image_dir):
                shutil.rmtree(image_dir)