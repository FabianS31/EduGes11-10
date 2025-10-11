from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno
from django.contrib import messages
from django.http import JsonResponse

def alta_alumno(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        tutor = request.POST.get('tutor')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        nivel = request.POST.get('nivel')

        Alumno.objects.create(
            nombre=nombre,
            apellido=apellido,
            tutor=tutor,
            direccion=direccion,
            telefono=telefono,
            nivel=nivel
        )

        messages.success(request, "Alta realizada correctamente.")
        return redirect('registros')
    
    return render(request, 'registros.html')


def detalle_alumno(request, legajo):
    try:
        alumno = Alumno.objects.get(ID_Legajo=legajo)
        data = {
            'ID_Legajo': alumno.ID_Legajo,
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'tutor': alumno.tutor,
            'direccion': alumno.direccion,
            'telefono': alumno.telefono,
            'nivel': alumno.nivel,
            'fecha_alta': alumno.fecha_alta.strftime('%d/%m/%Y %H:%M')
        }
        return JsonResponse(data)
    except Alumno.DoesNotExist:
        return JsonResponse({'error': 'Alumno no encontrado'})


def buscar_alumno(request):
    alumnos = Alumno.objects.all()
    query = request.GET.get('query')
    ID_Legajo = request.GET.get('ID_Legajo')
    resultados = []

    if query:
        resultados = alumnos.filter(nombre__icontains=query) | alumnos.filter(apellido__icontains=query)
    elif ID_Legajo:
        resultados = alumnos.filter(ID_Legajo=ID_Legajo)

    # Para autocompletar
    nombres_completos = [f"{a.nombre} {a.apellido}" for a in alumnos]
    legajos = [a.ID_Legajo for a in alumnos]

    return render(request, 'registros.html', {
        'alumnos': alumnos,
        'resultados': resultados,
        'nombres_completos': nombres_completos,
        'legajos': legajos,
        'query': query or '',
        'ID_Legajo': ID_Legajo or ''
    })
