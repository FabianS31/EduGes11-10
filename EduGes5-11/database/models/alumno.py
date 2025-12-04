from django.db import models

class Alumno(models.Model):
    legajo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50, blank=True, null=True)
    sala = models.CharField(max_length=50, blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)
    tipo_doc = models.CharField(max_length=20, blank=True, null=True)
    nro_doc = models.CharField(max_length=20, blank=True, null=True)
    calle = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    piso = models.CharField(max_length=10, blank=True, null=True)
    departamento = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    tutores = models.ManyToManyField("Tutor", related_name="alumnos", blank=True)

    def __str__(self):
        return f"{self.legajo} - {self.nombre} {self.apellido}"
