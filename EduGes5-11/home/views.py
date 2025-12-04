from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from database.models import Alumno, Tutor  # Importamos desde la nueva app 'database'
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


# -------- LOGIN --------
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return self.get_redirect_url() or '/'


# -------- PÁGINAS --------
@login_required
def home(request):
    return render(request, 'home/home.html')

# -------- ALUMNOS --------
@login_required
def alta_alumnos(request):
    year_actual = datetime.today().year
    return render(request, 'home/alumnos/alta_alumnos.html', {'year_actual': year_actual})

@login_required
def modificar_alumnos(request):
    alumno = None
    if request.method == 'POST':
        nombre_apellido = request.POST.get('nombre_apellido', '').strip()
        legajo = request.POST.get('legajo', '').strip()

        # --- Si se está guardando una modificación ---
        if 'id' in request.POST:
            try:
                alumno_id = int(request.POST.get('id'))
                alumno = Alumno.objects.get(id=alumno_id)

                # Obtención de datos (SIN 'tutor')
                campos = {
                    'nombre': request.POST.get('nombre', '').strip(),
                    'apellido': request.POST.get('apellido', '').strip(),
                    # 'tutor' SE HA QUITADO
                    'nivel': request.POST.get('nivel', '').strip(),
                    'sala': request.POST.get('sala', '').strip(),
                    'fecha_nac': request.POST.get('fecha_nac', '').strip(),
                    'tipo_doc': request.POST.get('tipo_doc', '').strip(),
                    'nro_doc': request.POST.get('nro_doc', '').strip(),
                    'calle': request.POST.get('calle', '').strip(),
                    'numero': request.POST.get('numero', '').strip(),
                    'piso': request.POST.get('piso', '').strip(),
                    'departamento': request.POST.get('departamento', '').strip(),
                    'telefono': request.POST.get('telefono', '').strip(),
                    'email': request.POST.get('email', '').strip()
                }

                # Patrones de validación (SIN 'tutor')
                patrones = {
                    'nombre': r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
                    'apellido': r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
                    # 'tutor' SE HA QUITADO
                    'sala': r'^[A-Za-z0-9 ]*$',
                    'nro_doc': r'^\d+$',
                    'numero': r'^\d*$',
                    'piso': r'^\d*$',
                    'telefono': r'^\d*$',
                    'email': r'^.+@.+\..+$'
                }

                # Validaciones y asignación
                for campo, valor in campos.items():
                    if valor: # Solo actualiza si el campo no está vacío
                        # ... (tu lógica de validación de patrones, fecha, nro_doc, telefono...)
                        # ... (esta parte no necesita cambios)
                        
                        # (Tu código de validación original)
                        if campo in patrones and not re.match(patrones[campo], valor):
                            messages.error(request, f"Valor inválido en {campo}.")
                            return render(request, 'home/alumnos/modificar_alumnos.html', {'alumno': alumno})
                        if campo == 'fecha_nac':
                            try:
                                valor = datetime.strptime(valor, "%Y-%m-%d").date()
                            except ValueError:
                                messages.error(request, "Formato de fecha inválido (AAAA-MM-DD).")
                                return render(request, 'home/alumnos/modificar_alumnos.html', {'alumno': alumno})
                        if campo == 'nro_doc':
                            tipo_doc = campos.get('tipo_doc', alumno.tipo_doc)
                            nro_doc_digits = re.sub(r'\D', '', valor)
                            if tipo_doc.upper() in ['DNI', 'DNI ARGENTINO', 'DNI Argentino']:
                                if not re.fullmatch(r'\d{7,8}', nro_doc_digits):
                                    messages.error(request, "Para DNI argentino ingrese 7 u 8 números (sin puntos).")
                                    return render(request, 'home/alumnos/modificar_alumnos.html', {'alumno': alumno})
                            else:
                                if not re.fullmatch(r'\d{6,12}', nro_doc_digits):
                                    messages.error(request, "Número de documento inválido. Para documento extranjero ingrese entre 6 y 12 dígitos.")
                                    return render(request, 'home/alumnos/modificar_alumnos.html', {'alumno': alumno})
                            valor = nro_doc_digits
                        if campo == 'telefono':
                            tel_digits = re.sub(r'\D', '', valor)
                            if not re.fullmatch(r'\d{7,15}', tel_digits):
                                messages.error(request, "Teléfono inválido. Debe contener entre 7 y 15 dígitos.")
                                return render(request, 'home/alumnos/modificar_alumnos.html', {'alumno': alumno})
                            valor = tel_digits
                        
                        # Asigna el valor al objeto alumno
                        setattr(alumno, campo, valor)

                alumno.save()
                messages.success(request, f"✅ Alumno {alumno.nombre} {alumno.apellido} modificado correctamente.")
                return redirect('modificar_alumnos')

            except Alumno.DoesNotExist:
                messages.error(request, "Alumno no encontrado.")
                return redirect('modificar_alumnos')

        # --- Si se está buscando un alumno ---
        if legajo:
            try:
                alumno = Alumno.objects.get(legajo__iexact=legajo) # Usar iexact es mejor
            except Alumno.DoesNotExist:
                messages.error(request, f"No se encontró alumno con legajo {legajo}.")
        elif nombre_apellido:
            alumnos = Alumno.objects.filter(nombre__icontains=nombre_apellido) | Alumno.objects.filter(apellido__icontains=nombre_apellido)
            if alumnos.exists():
                alumno = alumnos.first()
            else:
                messages.error(request, f"No se encontró alumno con nombre/apellido '{nombre_apellido}'.")
        else:
            messages.error(request, "Complete al menos un campo para buscar.")

    return render(request, 'home/alumnos/modificar_alumnos.html', {'alumno': alumno})

@login_required
def baja_alumnos(request):
    alumno = None
    if request.method == 'POST':
        nombre_apellido = request.POST.get('nombre_apellido', '').strip()
        legajo = request.POST.get('legajo', '').strip()
        if 'confirmar_baja' in request.POST:
            try:
                alumno_id = int(request.POST.get('id'))
                alumno = Alumno.objects.get(id=alumno_id)
                alumno.delete()
                messages.success(request, f"Alumno {alumno.nombre} {alumno.apellido} dado de baja correctamente.")
                return redirect('baja_alumnos')
            except Alumno.DoesNotExist:
                messages.error(request, "Alumno no encontrado.")
                return redirect('baja_alumnos')
        if legajo:
            try:
                alumno = Alumno.objects.get(legajo__iexact=legajo) # Usar iexact es mejor
            except Alumno.DoesNotExist:
                messages.error(request, f"No se encontró alumno con legajo {legajo}.")
        elif nombre_apellido:
            alumnos = Alumno.objects.filter(nombre__icontains=nombre_apellido) | Alumno.objects.filter(apellido__icontains=nombre_apellido)
            if alumnos.exists():
                alumno = alumnos.first()
            else:
                messages.error(request, f"No se encontró alumno con nombre/apellido '{nombre_apellido}'.")
    return render(request, 'home/alumnos/baja_alumnos.html', {'alumno': alumno})

@login_required
def guardar_alumno(request):
    if request.method == 'POST':
        legajo = (request.POST.get('legajo') or '').strip()
        apellido = (request.POST.get('apellido') or '').strip()
        nombre = (request.POST.get('nombre') or '').strip()
        # tutor = (request.POST.get('tutor') or '').strip() # <-- LÍNEA BORRADA
        nivel = (request.POST.get('nivel') or '').strip()
        sala = (request.POST.get('sala') or '').strip()
        fecha_nac_str = (request.POST.get('fecha_nac') or '').strip()
        tipo_doc = (request.POST.get('tipo_doc') or '').strip()
        nro_doc = (request.POST.get('nro_doc') or '').strip()
        calle = (request.POST.get('calle') or '').strip()
        numero = (request.POST.get('numero') or '').strip()
        piso = (request.POST.get('piso') or '').strip()
        departamento = (request.POST.get('departamento') or '').strip()
        telefono = (request.POST.get('telefono') or '').strip()
        email = (request.POST.get('email') or '').strip()

        required = {
            'Legajo': legajo,
            'Apellido': apellido,
            'Nombre': nombre,
            'Fecha de nacimiento': fecha_nac_str,
            'Tipo de documento': tipo_doc,
            'Número de documento': nro_doc,
            'Calle': calle,
            'Número de calle': numero,
            'Teléfono': telefono,
            'Email': email
            # Ya no se requiere 'Tutor' aquí
        }
        # ... (El resto de tu lógica de validación es correcta) ...
        
        faltantes = [k for k, v in required.items() if not v]
        if faltantes:
            messages.error(request, f"Complete los campos obligatorios: {', '.join(faltantes)}")
            return redirect('alta_alumnos')

        if not re.fullmatch(r'[A-Za-z0-9\-]+', legajo):
            messages.error(request, "El Legajo debe contener solo letras, números o guiones (ej. A-11).")
            return redirect('alta_alumnos')

        try:
            fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d").date()
            year_actual = datetime.today().year
            if fecha_nac.year < 1923 or fecha_nac.year > year_actual:
                messages.error(request, f"La fecha de nacimiento debe estar entre 1923 y {year_actual}.")
                return redirect('alta_alumnos')
        except ValueError:
            messages.error(request, "La fecha de nacimiento tiene un formato inválido. Debe ser AAAA-MM-DD.")
            return redirect('alta_alumnos')

        nro_doc_digits = re.sub(r'\D', '', nro_doc)
        if tipo_doc.upper() in ['DNI', 'DNI ARGENTINO', 'DNI Argentino']:
            if not re.fullmatch(r'\d{7,8}', nro_doc_digits):
                messages.error(request, "Para DNI argentino ingrese 7 u 8 números (sin puntos).")
                return redirect('alta_alumnos')
        else:
            if not re.fullmatch(r'\d{6,12}', nro_doc_digits):
                messages.error(request, "Número de documento inválido. Para documento extranjero ingrese entre 6 y 12 dígitos.")
                return redirect('alta_alumnos')

        tel_digits = re.sub(r'\D', '', telefono)
        if not re.fullmatch(r'\d{7,15}', tel_digits):
            messages.error(request, "Teléfono inválido. Debe contener entre 7 y 15 dígitos.")
            return redirect('alta_alumnos')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "El email ingresado no es válido (ej. usuario@dominio.com).")
            return redirect('alta_alumnos')

        if numero and not re.fullmatch(r'\d+', numero):
            messages.error(request, "El campo Número (dirección) debe contener solo números.")
            return redirect('alta_alumnos')

        try:
            Alumno.objects.create(
                legajo=legajo,
                nombre=nombre,
                apellido=apellido,
                # tutor=tutor, # <-- LÍNEA BORRADA
                nivel=nivel,
                sala=sala,
                fecha_nac=fecha_nac,
                tipo_doc=tipo_doc,
                nro_doc=nro_doc_digits,
                calle=calle,
                numero=numero,
                piso=piso,
                departamento=departamento,
                telefono=tel_digits,
                email=email
            )
            messages.success(request, f'Alumno {nombre} {apellido} dado de alta correctamente.')
        except IntegrityError:
            messages.error(request, f'Error: El legajo {legajo} o documento ya existe.')
        except Exception as e:
            messages.error(request, f'Error inesperado al guardar alumno: {str(e)}')

        return redirect('alta_alumnos')

    return redirect('alta_alumnos')

# -------- TUTORES --------
@login_required
def alta_tutores(request):
    # <-- LÓGICA AÑADIDA -->
    # Pasa la lista de alumnos al template para el selector
    todos_los_alumnos = Alumno.objects.all().order_by('apellido', 'nombre')
    context = {
        'alumnos_disponibles': todos_los_alumnos
    }
    return render(request, 'home/tutores/alta_tutores.html', context)

@login_required
def modificar_tutores(request):
    tutor = None
    tutor_alumnos_ids = []
    todos_los_alumnos = Alumno.objects.all().order_by('apellido', 'nombre')
    year_actual = datetime.today().year

    if request.method == 'POST':
        nombre_apellido = request.POST.get('nombre_apellido', '').strip()
        nro_doc_buscar = request.POST.get('nro_doc_buscar', '').strip()

        # --- Si se está guardando modificación ---
        if 'tutor_id' in request.POST:
            try:
                tutor_id = int(request.POST.get('tutor_id'))
                tutor = Tutor.objects.get(id=tutor_id)

                # Campos a actualizar
                campos = {
                    'apellido': request.POST.get('apellido', '').strip(),
                    'nombre': request.POST.get('nombre', '').strip(),
                    'fecha_nac': request.POST.get('fecha_nac', '').strip(),
                    'tipo_doc': request.POST.get('tipo_doc', '').strip(),
                    'nro_doc': request.POST.get('nro_doc', '').strip(),
                    'calle': request.POST.get('calle', '').strip(),
                    'numero': request.POST.get('numero', '').strip(),
                    'piso': request.POST.get('piso', '').strip(),
                    'departamento': request.POST.get('departamento', '').strip(),
                    'telefono': request.POST.get('telefono', '').strip(),
                    'email': request.POST.get('email', '').strip()
                }

                # Validaciones
                patrones = {
                    'nombre': r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
                    'apellido': r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
                    'nro_doc': r'^\d{6,12}$',
                    'numero': r'^\d*$',
                    'piso': r'^[A-Za-z0-9]*$',
                    'departamento': r'^[A-Za-z0-9]*$',
                    'telefono': r'^\d{7,15}$',
                    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|ar)$'
                }

                for campo, valor in campos.items():
                    if valor:
                        if campo in patrones and not re.fullmatch(patrones[campo], valor):
                            messages.error(request, f"Valor inválido en {campo}.")
                            return render(request, 'home/tutores/modificar_tutores.html', {
                                'tutor': tutor, 'alumnos': todos_los_alumnos,
                                'tutor_alumnos_ids': [a.id for a in tutor.alumnos.all()],
                                'year_actual': year_actual
                            })

                        if campo == 'fecha_nac':
                            try:
                                fecha_obj = datetime.strptime(valor, "%Y-%m-%d").date()
                                if fecha_obj.year < 1923 or fecha_obj.year > year_actual:
                                    messages.error(request, "Fecha fuera de rango.")
                                    return render(request, 'home/tutores/modificar_tutores.html', {
                                        'tutor': tutor, 'alumnos': todos_los_alumnos,
                                        'tutor_alumnos_ids': [a.id for a in tutor.alumnos.all()],
                                        'year_actual': year_actual
                                    })
                                valor = fecha_obj
                            except ValueError:
                                messages.error(request, "Formato de fecha inválido.")
                                return render(request, 'home/tutores/modificar_tutores.html', {
                                    'tutor': tutor, 'alumnos': todos_los_alumnos,
                                    'tutor_alumnos_ids': [a.id for a in tutor.alumnos.all()],
                                    'year_actual': year_actual
                                })

                        setattr(tutor, campo, valor)

                tutor.save()

                # Actualiza alumnos asignados
                ids_alumnos = request.POST.getlist('alumnos')
                if ids_alumnos:
                    alumnos_vincular = Alumno.objects.filter(id__in=ids_alumnos)
                    tutor.alumnos.set(alumnos_vincular)

                messages.success(request, f"Tutor {tutor.nombre} {tutor.apellido} modificado correctamente.")
                return redirect('modificar_tutores')

            except Tutor.DoesNotExist:
                messages.error(request, "Tutor no encontrado.")
                return redirect('modificar_tutores')

        # --- Si se está buscando ---
        else:
            if nombre_apellido:
                query = Q(nombre__icontains=nombre_apellido) | Q(apellido__icontains=nombre_apellido)
                tutores = Tutor.objects.filter(query)
                if tutores.exists():
                    tutor = tutores.first()
                    tutor_alumnos_ids = [a.id for a in tutor.alumnos.all()]
                else:
                    messages.error(request, f"No se encontró tutor con nombre/apellido '{nombre_apellido}'.")
            elif nro_doc_buscar:
                try:
                    tutor = Tutor.objects.get(nro_doc=nro_doc_buscar)
                    tutor_alumnos_ids = [a.id for a in tutor.alumnos.all()]
                except Tutor.DoesNotExist:
                    messages.error(request, f"No se encontró tutor con documento {nro_doc_buscar}.")
            else:
                messages.error(request, "Complete al menos un campo para buscar.")

    context = {
        'tutor': tutor,
        'alumnos': todos_los_alumnos,
        'tutor_alumnos_ids': tutor_alumnos_ids,
        'year_actual': year_actual
    }
    return render(request, 'home/tutores/modificar_tutores.html', context)

@login_required
def baja_tutores(request):
    tutor = None 
    context = {}

    if request.method == 'POST':
        if 'confirmar_baja' in request.POST:
            try:
                tutor_id = int(request.POST.get('tutor_id'))
                tutor_a_eliminar = Tutor.objects.get(id=tutor_id)
                nombre_completo = f"{tutor_a_eliminar.nombre} {tutor_a_eliminar.apellido}"
                tutor_a_eliminar.delete()
                
                messages.success(request, f"Tutor {nombre_completo} dado de baja correctamente.")
                
                return redirect('baja_tutores')
            except Tutor.DoesNotExist:
                
                messages.error(request, "Tutor no encontrado.")
                
                return redirect('baja_tutores')
            except Exception as e:
                
                messages.error(request, f"Error inesperado al dar de baja: {e}")
                
                return redirect('baja_tutores')

        else:
            nombre_apellido = request.POST.get('nombre_apellido', '').strip()
            nro_doc_buscar = request.POST.get('nro_doc_buscar', '').strip()

            if nombre_apellido:
                query = Q(nombre__icontains=nombre_apellido) | Q(apellido__icontains=nombre_apellido)
                tutores_encontrados = Tutor.objects.filter(query)
                if tutores_encontrados.exists():
                    tutor = tutores_encontrados.first()
                else:
                    
                    messages.error(request, f"No se encontró tutor con nombre/apellido '{nombre_apellido}'.")
                    
            elif nro_doc_buscar:
                try:
                    tutor = Tutor.objects.get(nro_doc=nro_doc_buscar)
                except Tutor.DoesNotExist:
                    
                    messages.error(request, f"No se encontró tutor con documento {nro_doc_buscar}.")
                    
            else:
                
                messages.error(request, "Complete al menos un campo para buscar.")
                
                
    context['tutor'] = tutor 
    return render(request, 'home/tutores/baja_tutores.html', context)

@login_required
def guardar_tutor(request):
    # Preparamos el contexto base por si hay errores
    todos_los_alumnos = Alumno.objects.all().order_by('apellido', 'nombre')
    context = {
        'alumnos_disponibles': todos_los_alumnos,
        'form_data': request.POST if request.method == 'POST' else None # Pasa los datos del POST si existen
    }

    if request.method == 'POST':
        # 1. Obtén todos los datos del tutor del POST
        apellido = request.POST.get('apellido')
        nombre = request.POST.get('nombre')
        fecha_nac_str = request.POST.get('fecha_nac')
        tipo_doc = request.POST.get('tipo_doc')
        nro_doc = request.POST.get('nro_doc')
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        piso = request.POST.get('piso')
        departamento = request.POST.get('departamento')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        # --- VALIDACIONES ANTES DE CREAR ---

        # 2. Validación de fecha
        fecha_nac = None
        if fecha_nac_str:
            try:
                fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d").date()
                year_actual = datetime.today().year
                if fecha_nac.year < 1923 or fecha_nac.year > year_actual:
                    messages.error(request, f"La fecha de nacimiento debe estar entre 1923 y {year_actual}.")
                    return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error
            except ValueError:
                messages.error(request, "Formato de fecha inválido. Debe ser AAAA-MM-DD.")
                return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error
        else:
             messages.error(request, "La fecha de nacimiento es obligatoria.")
             return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error


        # 3. Validación de Email (NUEVO)
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$"
        if not re.fullmatch(email_pattern, email):
            messages.error(request, 'Error: El formato del email no es válido o no termina en ".com".')
            return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error
        
        # (Aquí puedes añadir más validaciones: DNI, Teléfono, etc., usando re.fullmatch y devolviendo render si fallan)
        # Ejemplo validación DNI (6-12 dígitos):
        dni_pattern = r"^[0-9]{6,12}$"
        if not re.fullmatch(dni_pattern, nro_doc):
             messages.error(request, 'Error: El número de documento debe tener entre 6 y 12 dígitos.')
             return render(request, 'home/tutores/alta_tutores.html', context)

        # 4. Obtiene y valida la lista de alumnos
        ids_alumnos = request.POST.getlist('alumnos_seleccionados')
        if not ids_alumnos: # Si la lista está vacía
            messages.error(request, 'Error: Debe asignar al menos un alumno al tutor.')
            return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error

        # --- SI TODAS LAS VALIDACIONES PASAN, INTENTA CREAR ---
        try:
            nuevo_tutor = Tutor.objects.create(
                apellido=apellido,
                nombre=nombre,
                fecha_nac=fecha_nac,
                tipo_doc=tipo_doc,
                nro_doc=nro_doc,
                calle=calle,
                numero=numero,
                piso=piso,
                departamento=departamento,
                telefono=telefono,
                email=email
            )
                
            alumnos_a_vincular = Alumno.objects.filter(id__in=ids_alumnos)
            nuevo_tutor.alumnos.set(alumnos_a_vincular)

            messages.success(request, f'Tutor {nombre} {apellido} dado de alta y vinculado correctamente.')
            return redirect('alta_tutores') # Redirige solo si TODO fue exitoso

        except IntegrityError:
            messages.error(request, f'Error: El tutor con documento {tipo_doc} {nro_doc} ya existe.')
            return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error y datos
            
        except Exception as e:
            messages.error(request, f'Error inesperado al guardar tutor: {e}')
            return render(request, 'home/tutores/alta_tutores.html', context) # Re-render con error y datos

    # Si el método es GET (carga inicial)
    else:
        # Limpiamos form_data para que el formulario aparezca vacío
        context['form_data'] = None 
        return render(request, 'home/tutores/alta_tutores.html', context)
    
# -------- USUARIOS --------
# (Tus vistas de Usuario no necesitan cambios)
@login_required
def alta_usuario(request):
    return render(request, 'home/usuarios/alta_usuarios.html')

@login_required
def modificar_usuario(request):
    return render(request, 'home/usuarios/modificar_usuarios.html')

@login_required
def baja_usuario(request):
    return render(request, 'home/usuarios/baja_usuarios.html')

@login_required
def guardar_usuario(request):
    if request.method == 'POST':
        apellido = request.POST.get('apellido')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')

        try:
            User.objects.create_user(
                username=email,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password='EduGes123' # Considera usar un formulario de creación de usuario de Django
            )
            messages.success(request, f'Usuario {nombre} {apellido} creado correctamente.')
        except IntegrityError:
            messages.error(request, f'Error: Ya existe un usuario con el email {email}.')

        return redirect('alta_usuarios')

    return redirect('alta_usuarios')

# -------- PAGOS --------
# (Tu vista de Asignar Monto no necesita cambios)
@login_required
def asignar_monto(request):
    years = list(range(2023, 2101))
    selected_year = None
    february_data = None
    months_data = []

    MONTHS_FULL_LIST = [
        {"num": 2, "name": "Febrero", "label": "Monto - Febrero (Inscripción)"},
        {"num": 3, "name": "Marzo", "label": "Monto - Marzo"},
        {"num": 4, "name": "Abril", "label": "Monto - Abril"},
        {"num": 5, "name": "Mayo", "label": "Monto - Mayo"},
        {"num": 6, "name": "Junio", "label": "Monto - Junio"},
        {"num": 7, "name": "Julio", "label": "Monto - Julio"},
        {"num": 8, "name": "Agosto", "label": "Monto - Agosto"},
        {"num": 9, "name": "Septiembre", "label": "Monto - Septiembre"},
        {"num": 10, "name": "Octubre", "label": "Monto - Octubre"},
        {"num": 11, "name": "Noviembre", "label": "Monto - Noviembre"},
        {"num": 12, "name": "Diciembre", "label": "Monto - Diciembre"},
    ]

    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        selected_year = request.POST.get('selected_year')

        if selected_year:
            for month in MONTHS_FULL_LIST:
                month_info = {
                    'num': month['num'], 'name': month['name'], 'label': month['label'],
                    'value': request.POST.get(f'monto_{month["num"]}', '')
                }
                if month['num'] == 2:
                    february_data = month_info
                else:
                    months_data.append(month_info)

        if action_type == 'save_montos':
            messages.success(request, f"Montos año {selected_year} guardados (simulación).")
            return redirect('asignar_monto')

    context = {
        'years': years, 'february_data': february_data,
        'months_data': months_data, 'selected_year': selected_year,
    }
    return render(request, 'home/pagos/asignar_monto.html', context)

@login_required
def pagos_alumnos(request):
    
    context = {
        'years': list(range(2023, 2101)),
        'alumno': None,
        'selected_year': None,
        'meses_pago': None 
    }

    if request.method == 'POST' and request.POST.get('action_type') == 'search_student':
        nombre_apellido = request.POST.get('nombre_apellido', '').strip()
        legajo = request.POST.get('legajo', '').strip()
        alumno_encontrado = None

        try:
            if legajo:
                alumno_encontrado = Alumno.objects.filter(legajo__iexact=legajo).first()
                if not alumno_encontrado:
                    messages.error(request, f"No se encontró alumno con legajo {legajo}.")
            
            elif nombre_apellido:
                query = Q(nombre__icontains=nombre_apellido) | Q(apellido__icontains=nombre_apellido)
                alumno_encontrado = Alumno.objects.filter(query).first()
                if not alumno_encontrado:
                    messages.error(request, f"No se encontró alumno con nombre/apellido '{nombre_apellido}'.")
            
            else:
                messages.error(request, "Complete al menos un campo para buscar.")
        
        except Exception as e:
            messages.error(request, f"Error al buscar alumno: {e}")

        context['alumno'] = alumno_encontrado
        context['request.POST.nombre_apellido'] = nombre_apellido
        context['request.POST.legajo'] = legajo

    elif request.method == 'GET' and request.GET.get('alumno_id'):
        alumno_id = request.GET.get('alumno_id')
        selected_year = request.GET.get('selected_year')

        try:
            alumno = Alumno.objects.get(id=alumno_id)
            context['alumno'] = alumno
            context['selected_year'] = selected_year

            if selected_year:
                meses_simulados = []
                nombres_meses = ["", "", "Febrero (Inscripción)", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

                for i in range(2, 13): 
                    meses_simulados.append({
                        'num': i,
                        'nombre': nombres_meses[i],
                        'estado': 'Pendiente' 
                    })
                
                context['meses_pago'] = meses_simulados

        except Alumno.DoesNotExist:
            messages.error(request, "Error: Alumno no encontrado al cargar año.")
            # --- CORRECCIÓN CRÍTICA AQUÍ ---
            # Apuntaba a 'modificar_monto'
            return redirect('pagos_alumnos') 

    elif request.method == 'POST' and request.POST.get('action_type') == 'save_payments':
        alumno_id = request.POST.get('alumno_id')
        selected_year = request.POST.get('selected_year')
        
        alumno_nombre = "el alumno"
        try:
            alumno = Alumno.objects.get(id=alumno_id)
            alumno_nombre = f"{alumno.nombre} {alumno.apellido}"
        except Alumno.DoesNotExist:
            pass 
        
        messages.success(request, f"Simulación: Pagos del año {selected_year} para {alumno_nombre} guardados.")
        
        return redirect(f"{request.path}?alumno_id={alumno_id}&selected_year={selected_year}")

    
    return render(request, 'home/pagos/pagos_alumnos.html', context)

# -------- REPORTES --------
# (Tus vistas de Reportes no necesitan cambios)
@login_required
def tutores_vencida(request):
    return render(request, 'home/reportes/tutores_vencida.html')

@login_required
def cantidad_vencidas(request):
    return render(request, 'home/reportes/cantidad_vencidas.html')

@login_required
def alumnos_dia(request):
    return render(request, 'home/reportes/alumnos_dia.html')
