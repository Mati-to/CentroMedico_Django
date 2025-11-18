from django.db import models
from django.contrib.auth.models import User


class Especialidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    nombre_completo = models.CharField(max_length=100)
    rut = models.CharField(max_length=10, unique=True, error_messages={
        "unique": "El RUT ya está asociado a un médico en el sistema."
    })
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name="medico_especialidad")
    correo = models.EmailField(unique=True, error_messages={
        "unique": "El correo ya está asociado a un médico en el sistema.",
    })
    telefono = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        ordering = ["nombre_completo"]

    def __str__(self):
        return self.nombre_completo


class Paciente(models.Model):
    OPCIONES_SEXO = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro")
    ]
    nombre_completo = models.CharField(max_length=100)
    rut = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(choices=OPCIONES_SEXO, max_length=1, default="O")  
    telefono = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.nombre_completo

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="cita_paciente")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="cita_medico")
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name="cita_especialidad")
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    observaciones = models.TextField(max_length=400, null=True, blank=True)

    def __str__(self):
        return f"Cita del paciente {self.paciente} - Médico: {self.medico} - Fecha/hora: {self.fecha_cita} {self.hora_cita}"


# Perfil del usuario

class Usuario(models.Model):
    ROLES = [
        ("admin", "Administrador"),
        ("usuario", "Usuario común")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, default="usuario")

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
