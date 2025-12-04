from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    # Mantenemos el label original para preservar migraciones y la BD
    label = 'usuarios'
