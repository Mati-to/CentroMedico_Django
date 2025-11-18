from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from ..models import Medico
from ..forms import MedicoForm


class MedicoCreateView(LoginRequiredMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medico_form.html"
    success_url = reverse_lazy("medico_list")

    def form_valid(self, form):
        messages.success(self.request, "Médico creado con éxito.")
        return super().form_valid(form)


class MedicoUpdateView(LoginRequiredMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medico_form.html"
    success_url = reverse_lazy("medico_list")

    def form_valid(self, form):
        messages.success(self.request, "Médico actualizado con éxito.")
        return super().form_valid(form)


class MedicoListView(LoginRequiredMixin, ListView):
    model = Medico
    template_name = "medico_list.html"
    context_object_name = "medicos"

class MedicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medico
    template_name = "confirmar_eliminar.html"
    success_url = reverse_lazy("medico_list")

    def form_valid(self, form):
        messages.success(self.request, "Médico eliminado.")
        return super().form_valid(form)
