from django import forms
from core.models import Certificado, Evento, EventoTipo, Usuario, UsuarioTipo
from django.utils import timezone


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["tipo", "nome", "data_inicio", "data_fim", "local"]

        widgets = {
            "tipo": forms.Select(
                attrs={"class": "form-control"}, choices=EventoTipo.choices
            ),
            "nome": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do evento"}
            ),
            "data_inicio": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "data_fim": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "local": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Local do evento"}
            ),
        }

        labels = {
            "tipo": "Tipo de Evento",
            "nome": "Nome do Evento",
            "data_inicio": "Data e Hora de Início",
            "data_fim": "Data e Hora de Término",
            "local": "Local",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            now = timezone.now()
            self.fields["data_inicio"].initial = now
            self.fields["data_fim"].initial = now


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ["evento", "usuario"]

    def __init__(self, *args, **kwargs):
        organizador = kwargs.pop("organizador", None)
        super().__init__(*args, **kwargs)

        if organizador:
            self.fields["evento"].queryset = Evento.objects.filter(
                organizador=organizador
            )

            # self.fields["usuario"].queryset = self.fields["usuario"].queryset.none()
