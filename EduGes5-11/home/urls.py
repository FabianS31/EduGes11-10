from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # ALUMNOS (ahora usan modelos desde 'database')
    path('alumnos/alta/', views.alta_alumnos, name='alta_alumnos'),
    path('alumnos/modificar/', views.modificar_alumnos, name='modificar_alumnos'),
    path('alumnos/baja/', views.baja_alumnos, name='baja_alumnos'),
    path('alumnos/guardar/', views.guardar_alumno, name='guardar_alumno'),

    # TUTORES
    path('tutores/alta/', views.alta_tutores, name='alta_tutores'),
    path('tutores/modificar/', views.modificar_tutores, name='modificar_tutores'),
    path('tutores/baja/', views.baja_tutores, name='baja_tutores'),
    path('tutores/guardar/', views.guardar_tutor, name='guardar_tutor'),

    # USUARIOS
    path('usuarios/alta/', views.alta_usuario, name='alta_usuarios'),
    path('usuarios/modificar/', views.modificar_usuario, name='modificar_usuarios'),
    path('usuarios/baja/', views.baja_usuario, name='baja_usuarios'),
    path('usuarios/guardar/', views.guardar_usuario, name='guardar_usuario'),

    # PAGOS
    path('pagos/asignar_monto/', views.asignar_monto, name='asignar_monto'),
    path('pagos/pagos_alumnos/', views.pagos_alumnos, name='pagos_alumnos'),

    # REPORTES
    path('reportes/tutores_vencida/', views.tutores_vencida, name='tutores_vencida'),
    path('reportes/cantidad_vencidas/', views.cantidad_vencidas, name='cantidad_vencidas'),
    path('reportes/alumnos_dia/', views.alumnos_dia, name='alumnos_dia'),
]
