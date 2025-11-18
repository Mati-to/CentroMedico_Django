from django.urls import path
from .views import index, registro, login_usuario, logout_usuario
from .controllers import viewsMedico as viMed
from .controllers import viewsPaciente as viPac
from .controllers import viewsCita as viCit
from .controllers import viewsEspecialidad as viEsp

urlpatterns = [
    # Auth
    path("registro/", registro, name="registro"),
    path("login/", login_usuario, name="login"),
    path("logout/", logout_usuario, name="logout"),

    path("home/", index, name="index"),

    # Medicos
    path("medico/", viMed.MedicoListView.as_view(), name="medico_list"),
    path("medico/nuevo/", viMed.MedicoCreateView.as_view(), name="medico_create"),
    path("medico/editar/<int:pk>", viMed.MedicoUpdateView.as_view(), name="medico_update"),
    path("medico/eliminar/<int:pk>", viMed.MedicoDeleteView.as_view(), name="medico_delete"),

    # Pacientes
    path("paciente/", viPac.PacienteListView.as_view(), name="paciente_list"),
    path("paciente/nuevo/", viPac.PacienteCreateView.as_view(), name="paciente_create"),
    path("paciente/editar/<int:pk>", viPac.PacienteUpdateView.as_view(), name="paciente_update"),
    path("paciente/eliminar/<int:pk>", viPac.PacienteDeleteView.as_view(), name="paciente_delete"),

    # Citas medicas
    path("cita/", viCit.CitaListView.as_view(), name="cita_list"),
    path("cita/nueva/", viCit.CitaCreateView.as_view(), name="cita_create"),
    path("cita/editar/<int:pk>", viCit.CitaUpdateView.as_view(), name="cita_update"),
    path("cita/eliminar/<int:pk>", viCit.CitaDeleteView.as_view(), name="cita_delete"),

    # Especialidades medicas
    path("especialidad/", viEsp.EspecialidadListView.as_view(), name="especialidad_list"),
    path("especialidad/nueva/", viEsp.EspecialidadCreateView.as_view(), name="especialidad_create"),
    path("especialidad/editar/<int:pk>", viEsp.EspecialidadUpdateView.as_view(), name="especialidad_update"),
    path("especialidad/eliminar/<int:pk>", viEsp.EspecialidadDeleteView.as_view(), name="especialidad_delete")

]