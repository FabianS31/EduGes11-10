from django.db import models

class Tutor(models.Model):
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    fecha_nac = models.DateField()
    tipo_doc = models.CharField(max_length=20)
    nro_doc = models.CharField(max_length=20, unique=True)
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    piso = models.CharField(max_length=10, blank=True, null=True)
    departamento = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
