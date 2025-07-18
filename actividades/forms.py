# actividades/forms.py
from django import forms
from .models import Inscripcion, Alumno, Actividad
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AlumnoSignUpForm(UserCreationForm):
    nombre_completo = forms.CharField(max_length=200, help_text="Tu nombre completo")
    correo = forms.EmailField(help_text="Tu correo electrónico")
    curso = forms.CharField(max_length=50, help_text="Tu curso (ej. 3º ESO, Bachillerato)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('nombre_completo', 'correo', 'curso',)

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Alumno.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Ya existe un alumno con este correo electrónico.")
        return correo

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            alumno = Alumno.objects.create(
                usuario=user,
                nombre_completo=self.cleaned_data['nombre_completo'],
                correo=self.cleaned_data['correo'],
                curso=self.cleaned_data['curso']
            )
        return user

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'monitor', 'plazas_maximas', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }
        
class AdminAlumnoForm(forms.ModelForm):
    # Formulario para editar un Alumno (perfil)
    class Meta:
        model = Alumno
        fields = ['nombre_completo', 'correo', 'curso'] # No se edita el usuario aquí directamente

class AdminUserForm(forms.ModelForm):
    # Formulario para editar propiedades del User, incluyendo is_staff (para monitores)
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active'] # Añadimos is_active para activar/desactivar usuarios
        # Puedes añadir más campos como first_name, last_name si los usas

class AdminInscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['alumno', 'actividad']