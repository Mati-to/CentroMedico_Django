from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from ..models import Paciente
from ..forms import PacienteForm


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente_form.html"
    success_url = reverse_lazy("paciente_list")

    def form_valid(self, form):
        messages.success(self.request, "Paciente creado con éxito.")
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente_form.html"
    success_url = reverse_lazy("paciente_list")

    def form_valid(self, form):
        messages.success(self.request, "Paciente actualizado con éxito.")
        return super().form_valid(form)


class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "paciente_list.html"
    context_object_name = "pacientes"

class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = "confirmar_eliminar.html"
    success_url = reverse_lazy("paciente_list")

    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado.")
        return super().form_valid(form)