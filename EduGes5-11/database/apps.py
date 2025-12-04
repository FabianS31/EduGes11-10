from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'
    # Mantener label 'alumnos' para preservar migraciones y la BD
    label = 'alumnos'
