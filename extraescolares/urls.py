# extraescolares/urls.py
from django.contrib import admin
from django.urls import path, include
from actividades import views as actividades_views # Importa las vistas de actividades

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', actividades_views.lista_actividades, name='lista_actividades'), # Página de inicio
    path('actividades/', include('actividades.urls')), # Incluye las URLs de la app actividades
    path('accounts/', include('django.contrib.auth.urls')), # URLs para autenticación de Django (login, logout, password reset)
    path('signup/', actividades_views.user_signup, name='signup'),
    path('login/', actividades_views.user_login, name='login'),
    path('logout/', actividades_views.user_logout, name='logout'),
]
