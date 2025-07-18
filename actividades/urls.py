# actividades/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- URLs usuario ---
    path('inscribirse/<int:actividad_id>/', views.inscribirse_actividad, name='inscribirse_actividad'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('monitor/actividades/', views.actividades_monitor, name='actividades_monitor'),
   
    # --- URLs del Administrador ---
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/actividades/', views.admin_lista_actividades, name='admin_lista_actividades'),
    path('admin-dashboard/actividades/crear/', views.admin_crear_actividad, name='admin_crear_actividad'),
    path('admin-dashboard/actividades/editar/<int:pk>/', views.admin_editar_actividad, name='admin_editar_actividad'),
    path('admin-dashboard/actividades/borrar/<int:pk>/', views.admin_borrar_actividad, name='admin_borrar_actividad'),
   
    # Gestión de Monitores
    path('admin-dashboard/monitores/', views.admin_lista_monitores, name='admin_lista_monitores'),
    path('admin-dashboard/monitores/crear/', views.admin_crear_monitor, name='admin_crear_monitor'),
    path('admin-dashboard/monitores/editar/<int:pk>/', views.admin_editar_monitor, name='admin_editar_monitor'),
    path('admin-dashboard/monitores/borrar/<int:pk>/', views.admin_borrar_monitor, name='admin_borrar_monitor'),

    # Gestión de Alumnos
    path('admin-dashboard/alumnos/', views.admin_lista_alumnos, name='admin_lista_alumnos'),
    path('admin-dashboard/alumnos/crear/', views.admin_crear_alumno, name='admin_crear_alumno'),
    path('admin-dashboard/alumnos/editar/<int:pk>/', views.admin_editar_alumno, name='admin_editar_alumno'),
    path('admin-dashboard/alumnos/borrar/<int:pk>/', views.admin_borrar_alumno, name='admin_borrar_alumno'),

    # Gestión de Inscripciones
    path('admin-dashboard/inscripciones/', views.admin_lista_inscripciones, name='admin_lista_inscripciones'),
    path('admin-dashboard/inscripciones/crear/', views.admin_crear_inscripcion, name='admin_crear_inscripcion'),
    path('admin-dashboard/inscripciones/editar/<int:pk>/', views.admin_editar_inscripcion, name='admin_editar_inscripcion'),
    path('admin-dashboard/inscripciones/borrar/<int:pk>/', views.admin_borrar_inscripcion, name='admin_borrar_inscripcion'),
]
