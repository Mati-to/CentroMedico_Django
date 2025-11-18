import re
from django.core.exceptions import ValidationError

def validar_nombre_completo(nombre) -> str:
    nombre = nombre.strip()
    palabras: list[str] = nombre.split()

    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", nombre):
        raise ValidationError("Nombre inválido. Solo debe contener letras espacios.")

    if len(palabras) < 2:
        raise ValidationError("El nombre debe tener al menos nombre y apellido.")
    
    for p in palabras:
        if len(p) < 3:
            raise ValidationError("Cada palabra debe tener al menos 3 caracteres.")
    
    return nombre

def validar_rut(rut) -> str:
    rut = rut.strip()

    if not re.match(r"^\d{7,8}-[\dkK]$", rut):
        raise ValidationError("RUT inválido. Intente nuevamente.")

    return rut


def validar_telefono(telefono) -> str:
    telefono = telefono.strip()

    if not re.match(r'^\d{9,15}$', telefono):
        raise ValidationError("Teléfono inválido. Solo debe contener números.")
     
    return telefono
