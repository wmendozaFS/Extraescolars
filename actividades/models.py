from django.db import models
from django.contrib.auth.models import User # Para la autenticación de usuarios

class Monitor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='monitor_profile')
    nombre_completo = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo
class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    monitor = models.ForeignKey(Monitor, on_delete=models.SET_NULL, null=True, blank=True)
    plazas_maximas = models.IntegerField()
    fecha_inicio = models.DateField()

    def plazas_restantes(self):
        inscripciones_actuales = self.inscripcion_set.count()
        return self.plazas_maximas - inscripciones_actuales

    def __str__(self): 
        return self.nombre
    
class Alumno(models.Model):
    # Enlazamos el Alumno con el modelo de usuario de Django para la autenticación
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    correo = models.EmailField(unique=True) # El correo será único
    curso = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_completo

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Asegura que un alumno no pueda inscribirse dos veces a la misma actividad
        unique_together = ('alumno', 'actividad')

    def __str__(self):
        return f"{self.alumno.nombre_completo} inscrito en {self.actividad.nombre}"