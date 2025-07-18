# actividades/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Actividad, Alumno, Inscripcion, Monitor
from .forms import (
    AlumnoSignUpForm,
    ActividadForm,
    AdminAlumnoForm,
    AdminUserForm,
    AdminInscripcionForm,
    UserCreationForm
)
from django.contrib.auth.models import User
from django.contrib.auth import login, logout # Importa login y logout
from django.contrib.auth.forms import AuthenticationForm # Importa el formulario de autenticación

# Decoradores para verificar roles
def is_alumno(user):
    return hasattr(user, 'alumno')

def is_monitor(user):
    return not hasattr(user, 'alumno') and user.is_staff # O user.groups.filter(name='Monitores').exists()

def is_admin(user):
    return user.is_authenticated and user.is_staff

def lista_actividades(request):
    actividades_list = Actividad.objects.all().order_by('fecha_inicio')

    # Lógica de filtrado
    monitor_filter = request.GET.get('monitor')
    curso_filter = request.GET.get('curso')
    fecha_filter = request.GET.get('fecha')

    if monitor_filter:
        actividades_list = actividades_list.filter(monitor__nombre_completo__icontains=monitor_filter)
    if curso_filter:
        pass
    if fecha_filter:
        actividades_list = actividades_list.filter(fecha_inicio=fecha_filter)

    # Paginación
    paginator = Paginator(actividades_list, 5)  # 5 actividades por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'monitors': Actividad.objects.values_list('monitor', flat=True).distinct(),
    }
    return render(request, 'actividades/lista_actividades.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/') # Solo accesible para usuarios admin (is_staff)
def admin_dashboard(request):
    """
    Dashboard principal del administrador. Muestra un resumen y enlaces a la gestión de actividades.
    """
    total_actividades = Actividad.objects.count()
    total_alumnos = Alumno.objects.count()
    total_inscripciones = Inscripcion.objects.count()
    total_Monitores = Monitor.objects.count()

    context = {
        'total_actividades': total_actividades,
        'total_alumnos': total_alumnos,
        'total_inscripciones': total_inscripciones,
        'total_monitores': total_Monitores
    }
    return render(request, 'actividades/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_lista_actividades(request):
    """
    Muestra el listado de actividades para que el administrador las gestione (editar, borrar).
    """
    actividades = Actividad.objects.all().order_by('fecha_inicio')
    context = {
        'actividades': actividades
    }
    return render(request, 'actividades/admin_lista_actividades.html', context)


@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_crear_actividad(request):
    """
    Formulario para que el administrador cree una nueva actividad.
    """
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad creada exitosamente.')
            return redirect('admin_lista_actividades')
    else:
        form = ActividadForm()
    return render(request, 'actividades/admin_actividad_form.html', {'form': form, 'action': 'Crear'})


@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_editar_actividad(request, pk):
    """
    Formulario para que el administrador edite una actividad existente.
    """
    actividad = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad actualizada exitosamente.')
            return redirect('admin_lista_actividades')
    else:
        form = ActividadForm(instance=actividad)
    return render(request, 'actividades/admin_actividad_form.html', {'form': form, 'action': 'Actualizar'})


@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_borrar_actividad(request, pk):
    """
    Confirma y permite al administrador borrar una actividad.
    """
    actividad = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        actividad.delete()
        messages.success(request, 'Actividad eliminada exitosamente.')
        return redirect('admin_lista_actividades')
    return render(request, 'actividades/admin_borrar_actividad_confirm.html', {'actividad': actividad})

@login_required
@user_passes_test(is_alumno, login_url='/login/')
def inscribirse_actividad(request, actividad_id):
    """
    Formulario para que un alumno se inscriba a una actividad.
    Valida que no se inscriba dos veces y que haya plazas.
    """
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    alumno = request.user.alumno # Asumimos que el usuario logueado es un alumno

    if request.method == 'POST':
        if actividad.plazas_restantes() <= 0:
            messages.error(request, 'Lo sentimos, no quedan plazas disponibles para esta actividad.')
            return redirect('lista_actividades')

        try:
            # Crear la instancia de Inscripcion directamente
            inscripcion = Inscripcion.objects.create(
                alumno=alumno,
                actividad=actividad
            )
            messages.success(request, f'¡Te has inscrito correctamente en {actividad.nombre}!')
            return redirect('mis_inscripciones')
        except IntegrityError:
            messages.warning(request, f'Ya estás inscrito en {actividad.nombre}.')
            return redirect('lista_actividades')
    else:
        pass

    context = {
        'actividad': actividad,
        # No pasamos 'form' al contexto porque no hay campos que el usuario deba rellenar
    }
    return render(request, 'actividades/inscribirse_actividad.html', context)

@login_required
@user_passes_test(is_alumno, login_url='/login/') # Solo para alumnos logueados
def mis_inscripciones(request):
    """
    Muestra las actividades en las que se ha inscrito el alumno logueado.
    """
    alumno = request.user.alumno
    inscripciones = Inscripcion.objects.filter(alumno=alumno).order_by('-fecha_inscripcion')
    context = {
        'inscripciones': inscripciones
    }
    return render(request, 'actividades/mis_inscripciones.html', context)

# Vistas de autenticación
def user_signup(request):
    if request.method == 'POST':
        form = AlumnoSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Inicia sesión al usuario recién registrado
            messages.success(request, "¡Tu cuenta ha sido creada exitosamente!")
            return redirect('lista_actividades')
    else:
        form = AlumnoSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}!")
            return redirect('lista_actividades')
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('lista_actividades')

@login_required
@user_passes_test(is_monitor, login_url='/login/')
def actividades_monitor(request):
    try:
        monitor_actual = request.user.monitor_profile
        actividades = Actividad.objects.filter(monitor=monitor_actual)
        
    except Monitor.DoesNotExist:
            actividades = [] 
    context = {
        'actividades': actividades
    }
    return render(request, 'actividades/actividades_monitor.html', context)

# --- Gestión de Monitores ---
@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_lista_monitores(request):
    # Monitores son usuarios staff que no son alumnos (simplificación)
    monitores = User.objects.filter(is_staff=True).exclude(id__in=Alumno.objects.values_list('usuario__id', flat=True))
    context = {'monitores': monitores}
    return render(request, 'actividades/admin_lista_monitores.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_crear_monitor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Usamos UserCreationForm para crear el usuario
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True # Marca como monitor
            user.save()
            messages.success(request, 'Monitor creado exitosamente.')
            return redirect('admin_lista_monitores')
    else:
        form = UserCreationForm()
    return render(request, 'actividades/admin_monitor_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_editar_monitor(request, pk):
    monitor_user = get_object_or_404(User, pk=pk, is_staff=True)
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=monitor_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Monitor actualizado exitosamente.')
            return redirect('admin_lista_monitores')
    else:
        form = AdminUserForm(instance=monitor_user)
    return render(request, 'actividades/admin_monitor_form.html', {'form': form, 'action': 'Editar'})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_borrar_monitor(request, pk):
    monitor_user = get_object_or_404(User, pk=pk, is_staff=True)
    if request.method == 'POST':
        monitor_user.delete()
        messages.success(request, 'Monitor eliminado exitosamente.')
        return redirect('admin_lista_monitores')
    return render(request, 'actividades/admin_borrar_monitor_confirm.html', {'monitor': monitor_user})

# --- Gestión de Alumnos ---
@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_lista_alumnos(request):
    alumnos = Alumno.objects.all().order_by('nombre_completo')
    context = {'alumnos': alumnos}
    return render(request, 'actividades/admin_lista_alumnos.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoSignUpForm(request.POST) # Usamos el formulario de registro de alumno
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno creado exitosamente.')
            return redirect('admin_lista_alumnos')
    else:
        form = AlumnoSignUpForm()
    return render(request, 'actividades/admin_alumno_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        user_form = AdminUserForm(request.POST, instance=alumno.usuario)
        alumno_form = AdminAlumnoForm(request.POST, instance=alumno)
        if user_form.is_valid() and alumno_form.is_valid():
            user_form.save()
            alumno_form.save()
            messages.success(request, 'Alumno actualizado exitosamente.')
            return redirect('admin_lista_alumnos')
    else:
        user_form = AdminUserForm(instance=alumno.usuario)
        alumno_form = AdminAlumnoForm(instance=alumno)
    context = {
        'user_form': user_form,
        'alumno_form': alumno_form,
        'action': 'Editar',
        'alumno': alumno,
    }
    return render(request, 'actividades/admin_alumno_form.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_borrar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        # Borrar el Alumno automáticamente borra el User asociado (CASCADE)
        alumno.delete()
        messages.success(request, 'Alumno eliminado exitosamente.')
        return redirect('admin_lista_alumnos')
    return render(request, 'actividades/admin_borrar_alumno_confirm.html', {'alumno': alumno})

# --- Gestión de Inscripciones ---
@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_lista_inscripciones(request):
    inscripciones = Inscripcion.objects.all().order_by('-fecha_inscripcion')
    context = {'inscripciones': inscripciones}
    return render(request, 'actividades/admin_lista_inscripciones.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_crear_inscripcion(request):
    if request.method == 'POST':
        form = AdminInscripcionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Inscripción creada exitosamente.')
                return redirect('admin_lista_inscripciones')
            except IntegrityError:
                messages.error(request, 'El alumno ya está inscrito en esta actividad.')
    else:
        form = AdminInscripcionForm()
    return render(request, 'actividades/admin_inscripcion_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_editar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if request.method == 'POST':
        form = AdminInscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Inscripción actualizada exitosamente.')
                return redirect('admin_lista_inscripciones')
            except IntegrityError:
                messages.error(request, 'El alumno ya está inscrito en esta actividad.')
    else:
        form = AdminInscripcionForm(instance=inscripcion)
    return render(request, 'actividades/admin_inscripcion_form.html', {'form': form, 'action': 'Editar'})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_borrar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if request.method == 'POST':
        inscripcion.delete()
        messages.success(request, 'Inscripción eliminada exitosamente.')
        return redirect('admin_lista_inscripciones')
    return render(request, 'actividades/admin_borrar_inscripcion_confirm.html', {'inscripcion': inscripcion})