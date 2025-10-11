from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('ID_Legajo', 'nombre', 'apellido', 'nivel', 'tutor')
