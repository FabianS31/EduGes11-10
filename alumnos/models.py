from django.db import models

class Alumno(models.Model):
    ID_Legajo = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tutor = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    nivel = models.CharField(max_length=50, blank=True, null=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ID_Legajo} - {self.nombre} {self.apellido}"

# Create your models here.
