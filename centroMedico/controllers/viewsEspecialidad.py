from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from ..models import Especialidad
from ..forms import EspecialidadForm


class EspecialidadCreateView(LoginRequiredMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "especialidad_form.html"
    success_url = reverse_lazy("especialidad_list")

    def form_valid(self, form):
        messages.success(self.request, "Especialidad creada con éxito.")
        return super().form_valid(form)


class EspecialidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "especialidad_form.html"
    success_url = reverse_lazy("especialidad_list")

    def form_valid(self, form):
        messages.success(self.request, "Especialidad actualizada con éxito.")
        return super().form_valid(form)


class EspecialidadListView(LoginRequiredMixin, ListView):
    model = Especialidad
    template_name = "especialidad_list.html"
    context_object_name = "especialidades"

class EspecialidadDeleteView(LoginRequiredMixin, DeleteView):
    model = Especialidad
    template_name = "confirmar_eliminar.html"
    success_url = reverse_lazy("especialidad_list")

    def form_valid(self, form):
        messages.success(self.request, "Especialidad eliminada.")
        return super().form_valid(form)


