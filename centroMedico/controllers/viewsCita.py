from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from ..models import Cita
from ..forms import CitaForm, FiltroCitaForm


class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita_form.html"
    success_url = reverse_lazy("cita_list")

    def form_valid(self, form):
        messages.success(self.request, "Cita agendada con éxito.")
        return super().form_valid(form)


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita_form.html"
    success_url = reverse_lazy("cita_list")

    def form_valid(self, form):
        messages.success(self.request, "Cita actualizada con éxito.")
        return super().form_valid(form)


class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "cita_list.html"
    context_object_name = "citas"

    # Aplicación de los filtros usando Dynamic Filtering
    def get_queryset(self):
        queryset = super().get_queryset()
        medico = self.request.GET.get("medico")
        paciente = self.request.GET.get("paciente")
        fecha = self.request.GET.get("fecha_cita")

        if medico:
            queryset = queryset.filter(medico_id=medico)
        if paciente:
            queryset = queryset.filter(paciente_id=paciente)
        if fecha:
            queryset = queryset.filter(fecha_cita=fecha)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltroCitaForm(self.request.GET)
        return context


class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = "confirmar_eliminar.html"
    success_url = reverse_lazy("cita_list")

    def form_valid(self, form):
        messages.success(self.request, "Cita eliminada.")
        return super().form_valid(form)
