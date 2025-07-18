# **Gestion de Actividades Extraescolares**
### Desarrolle una aplicacion web con Django que permite a una escuela gestionar sus actividades extraescolares y que los alumnos puedan inscribirse en ellas
### Home y listado publico de Actividades con su nombre, descripcion, Fecha inicio y plazas restantes.
<img width="1911" height="902" alt="image" src="https://github.com/user-attachments/assets/65eb4011-d91e-4cfe-b8d8-461094b2c02c" />

## Autenticacion y Listado publico de Actividades, solicita inicio sesion para inscribirse
### Inicio de Sesion, autenticacion para alumnos y monitores
<img width="1917" height="902" alt="image" src="https://github.com/user-attachments/assets/7bfb8b14-a115-4011-acd9-aa7d8a372630" />

### Registro Nuevo Alumno, formulario para que un alumno se registre a la plataformax y se inscriba a la actividad, si ya esta registrado solo debe iniciar sesion
<img width="1917" height="902" alt="image" src="https://github.com/user-attachments/assets/762c102e-546a-4f08-a95f-bc17e295f052" />
<img width="1908" height="893" alt="image" src="https://github.com/user-attachments/assets/4f47103a-252f-4d6e-a201-fc77ca2ad816" />
<img width="1918" height="902" alt="image" src="https://github.com/user-attachments/assets/2ab0a7a7-8bf0-4b87-83c2-5fb181764e3d" />

### Confirmacion de inscripcion Exitosa!!, Listado de actividades en las que se encuentra inscrito el alumno
<img width="1912" height="902" alt="image" src="https://github.com/user-attachments/assets/9917f691-67cb-4029-8071-b297131e50d7" />
<img width="1908" height="887" alt="image" src="https://github.com/user-attachments/assets/195cb471-cfcf-4c4a-a32b-5d8be560b364" />

### Validacion que no se pueda inscribir mas de una vez en una actividad
<img width="1902" height="885" alt="image" src="https://github.com/user-attachments/assets/d298ba89-750c-4cd6-9d73-d671873b8eda" />

### Filtro por Monitor, filtro por monitor
<img width="1892" height="897" alt="image" src="https://github.com/user-attachments/assets/42d685f0-c4ef-4d5f-8ce3-55256ec9e46e" />

### Filtro por Fecha, Filtro por fecha
<img width="1911" height="900" alt="image" src="https://github.com/user-attachments/assets/d05beab0-5159-4d65-9b50-dce2ca2d07d9" />

## Dashboard Monitor
<img width="1911" height="897" alt="image" src="https://github.com/user-attachments/assets/fb4eb136-dc41-4030-89bf-0120ec6434c0" />

### Gestion Actividades
<img width="1917" height="902" alt="image" src="https://github.com/user-attachments/assets/acac3320-c44a-470c-b6db-bf03dd104e99" />

### Crear Nueva Actvidad
<img width="1901" height="896" alt="image" src="https://github.com/user-attachments/assets/75dba036-6ea8-4d2d-9a8d-3b01d8e73b72" />
<img width="1916" height="897" alt="image" src="https://github.com/user-attachments/assets/3479a9e7-63d3-4170-81db-d0759f154585" />

# Modelos models.py
```Python
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
```
## Formulario Para la Inscripcion reutilizo el formulario que muestra la actividad ActividadForm y en la plantilla agrego la accion (el boton inscribirse) tambien he creado AdminInscripcionForm para inscribir un alumno desde el panel de Monitor o de admin
```Python
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'monitor', 'plazas_maximas', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }

class AdminInscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['alumno', 'actividad']
```





