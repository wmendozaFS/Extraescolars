# actividades/admin.py
from django.contrib import admin
from .models import Actividad, Alumno, Inscripcion, Monitor

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'correo', 'especialidad', 'usuario')
    search_fields = ('nombre_completo', 'correo', 'especialidad')
@admin.register(Actividad)

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monitor', 'plazas_maximas', 'fecha_inicio', 'plazas_restantes')
    search_fields = ('nombre', 'monitor')
    list_filter = ('fecha_inicio', 'monitor')

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'correo', 'curso', 'usuario')
    search_fields = ('nombre_completo', 'correo', 'curso')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'actividad', 'fecha_inscripcion')
    list_filter = ('actividad', 'fecha_inscripcion')
    search_fields = ('alumno__nombre_completo', 'actividad__nombre')