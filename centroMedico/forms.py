import re
from django import forms
from datetime import date, time
from django.contrib.auth.models import User
from .validaciones import validar_nombre_completo, validar_telefono, validar_rut
from .models import Especialidad, Medico, Paciente, Cita, Usuario

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Ej: Pediatría"})
        }

    def clean_nombre(self) -> str:
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3 or len(nombre) > 50:
            raise forms.ValidationError("El nombre de la especialidad debe tener entre 3 a 50 caracteres.")
        return nombre
    
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ["nombre_completo", "rut", "especialidad", "correo", "telefono"]
        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "12111222-2"}),
            "especialidad": forms.Select(attrs={"class": "form-select"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"})
        }

    def clean_nombre_completo(self) -> str:
        nombre = self.cleaned_data["nombre_completo"]
        return validar_nombre_completo(nombre)
    
    def clean_rut(self) -> str:
        rut = self.cleaned_data["rut"]
        return validar_rut(rut)
    
    def clean_correo(self) -> str:
        correo = self.cleaned_data["correo"].strip()

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", correo):
            raise forms.ValidationError("Correo inválido. Intente nuevamente.")
        
        return correo
    
    def clean_telefono(self) -> str: 
        telefono = self.cleaned_data["telefono"]
        if telefono:
            return validar_telefono(telefono)
        else:
            return telefono
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     correo = cleaned_data.get("correo")

    #     if correo:
    #         medico = Medico.objects.filter(correo=correo)
    #         if self.instance.pk:
    #             medico = medico.exclude(pk=self.instance.pk)
    #         if medico.exists():
    #             raise forms.ValidationError("El correo ya está asociado a un médico en el sistema.")
            
    #     return cleaned_data


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nombre_completo", "rut", "fecha_nacimiento", "sexo", "telefono"]
        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexo": forms.Select(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"})
        }

    def clean_nombre_completo(self) -> str:
        nombre = self.cleaned_data["nombre_completo"]
        return validar_nombre_completo(nombre)
    
    def clean_rut(self) -> str:
        rut = self.cleaned_data["rut"]
        return validar_rut(rut)
    
    def clean_telefono(self) -> str: 
        telefono = self.cleaned_data["telefono"]
        if telefono:
            return validar_telefono(telefono)
        else:
            return telefono


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["paciente", "medico", "fecha_cita", "hora_cita", "observaciones"]
        widgets = {
            "paciente": forms.Select(attrs={"class": "form-control"}),
            "medico": forms.Select(attrs={"class": "form-control"}),
            "fecha_cita": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hora_cita": forms.TimeInput(attrs={
                "class": "form-control", 
                "type": "time", 
                "min": "09:00", 
                "max": "18:00"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": "1"})
        }

    def save(self, commit=True):
        cita = super().save(commit=False)
        cita.especialidad = cita.medico.especialidad
        if commit:
            cita.save()
        return cita
    
    def clean_fecha_cita(self) -> date:
        fecha_cita = self.cleaned_data["fecha_cita"]

        if fecha_cita < date.today():
            raise forms.ValidationError("La cita médica no puede ser anterior a la fecha de hoy.")
        
        return fecha_cita
    
    def clean_hora_cita(self) -> time:
        hora_cita = self.cleaned_data["hora_cita"]
        hora_entrada = time(9, 0)
        hora_salida = time(19, 0)

        if hora_cita < hora_entrada or hora_cita > hora_salida:
            raise forms.ValidationError("La hora de las citas es entre 09:00 y 19:00hrs.")
        
        return hora_cita
    
    def clean(self):
        cleaned_data = super().clean()
        medico = cleaned_data.get("medico")
        fecha_cita = cleaned_data.get("fecha_cita")
        hora_cita = cleaned_data.get("hora_cita")
        paciente = cleaned_data.get("paciente")

        if medico and fecha_cita and hora_cita:
            esDuplicado = Cita.objects.filter(medico=medico, fecha_cita=fecha_cita, hora_cita=hora_cita).exists()
            if esDuplicado:
                raise forms.ValidationError("Este médico ya tiene una cita agendada en ese horario.")
            
        if paciente and medico and fecha_cita:
            especialidad = medico.especialidad
            esDuplicado = Cita.objects.filter(paciente=paciente, especialidad=especialidad, fecha_cita=fecha_cita).exists()
            if esDuplicado:
                raise forms.ValidationError("El paciente ya tiene hora con esa especialidad en el día seleccionado.")

        return cleaned_data


# Formulario del filtro de citas
class FiltroCitaForm(forms.Form):
    medico = forms.ModelChoiceField(
        queryset=Medico.objects.all(),
        required=False,
        label="Médico",
        widget=forms.Select(attrs={"class": "form-select"}))
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        required=False,
        label="Paciente",
        widget=forms.Select(attrs={"class": "form-select"}))
    fecha_cita = forms.DateField(
        required=False,
        label="Fecha de cita",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

# Formularios para registro y login

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ]+$", username):
            raise forms.ValidationError("Nombre de usuario inválido.")

        if len(username) < 3:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 3 caracteres.")
        
        return username

    def clean_password(self):
        password = self.cleaned_data["password"].strip()

        if len(password) < 3:
            raise forms.ValidationError("Contraseña inválida.")
        
        return password
        

class RegistroForm(forms.ModelForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
    rol = forms.ChoiceField(choices=Usuario.ROLES)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Usuario.objects.create(
                user = user,
                rol = self.cleaned_data["rol"]
            )
        return user

