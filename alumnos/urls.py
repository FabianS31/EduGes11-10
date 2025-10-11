from django.urls import path
from . import views

urlpatterns = [
    path('alta/', views.alta_alumno, name='alta_alumno'),
    path('buscar/', views.buscar_alumno, name='buscar_alumno'),
    path('detalle/<int:legajo>/', views.detalle_alumno, name='detalle_alumno'),
]

