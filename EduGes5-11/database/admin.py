from django.contrib import admin
from .models.alumno import Alumno
from .models.tutor import Tutor


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = (
        'legajo',
        'apellido',
        'nombre',
        'nro_doc',
        'fecha_nac',
        'get_domicilio',
        'telefono',
    )
    search_fields = ('legajo', 'apellido', 'nombre', 'nro_doc')
    list_filter = ('nivel', 'sala')

    def get_domicilio(self, obj):
        partes = [obj.calle or '', obj.numero or '', obj.piso or '', obj.departamento or '']
        return " ".join(p for p in partes if p)
    get_domicilio.short_description = "Domicilio"


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'nro_doc', 'telefono', 'email')
    search_fields = ('apellido', 'nombre', 'nro_doc')
