from django.apps import AppConfig

class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
    # Configuración extendida para cambiar el nombre de la aplicación en el sector admin
    verbose_name = 'Contacto'   
