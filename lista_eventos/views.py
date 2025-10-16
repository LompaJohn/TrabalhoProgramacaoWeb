from datetime import datetime, timezone
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from core.models import Certificado, Evento, Inscricao, Usuario, UsuarioTipo
from .forms import CertificadoForm, EventoForm

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader


class OrganizadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and hasattr(self.request.user, "usuario")
            and self.request.user.usuario.tipo == UsuarioTipo.ORGANIZADOR
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        elif not hasattr(self.request.user, "usuario"):
            messages.error(
                self.request, "Você precisa completar seu perfil de usuário."
            )
        else:
            messages.error(self.request, "Apenas organizadores podem criar eventos.")
        return redirect("pagina-inicial")


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "lista_eventos.html"
    context_object_name = "eventos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, "usuario"):

            context["user_inscricoes"] = [
                x.evento.id
                for x in Inscricao.objects.filter(usuario=self.request.user.usuario)
            ]
        else:
            context["user_inscricoes"] = []
        return context


class EventoCreateView(LoginRequiredMixin, OrganizadorRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_form.html"
    success_url = reverse_lazy("lista-eventos")

    def form_valid(self, form):
        form.instance.organizador = self.request.user.usuario
        response = super().form_valid(form)
        return response


class EventoUpdateView(LoginRequiredMixin, OrganizadorRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_form.html"
    success_url = reverse_lazy("lista-eventos")


@login_required
def inscrever_evento_view(request: HttpRequest, pk: int):
    evento = get_object_or_404(Evento, id=pk)

    if not hasattr(request.user, "usuario"):
        messages.error(request, "Você precisa completar seu perfil de usuário.")
        return redirect("lista-eventos")

    if request.user.usuario.tipo == UsuarioTipo.ORGANIZADOR:
        messages.error(request, "Organizadores não podem se inscrever em eventos.")
        return redirect("lista-eventos")

    if Inscricao.objects.filter(usuario=request.user.usuario, evento=evento).exists():
        messages.warning(request, f"Você já está inscrito no evento {evento.nome}.")
        return redirect("lista-eventos")

    if Certificado.objects.filter(usuario=request.user.usuario, evento=evento).exists():
        messages.warning(
            request, f"Você já tem um certificado desse evento {evento.nome}."
        )
        return redirect("lista-eventos")

    if evento.data_fim < datetime.now(timezone.utc):
        messages.warning(request, f"Esse evento já passou {evento.nome}.")
        return redirect("lista-eventos")

    Inscricao.objects.create(usuario=request.user.usuario, evento=evento)

    evento.participantes += 1
    evento.save()

    messages.success(
        request, f"Inscrição no evento {evento.nome} realizada com sucesso!"
    )

    return redirect("lista-eventos")


@login_required
def desinscrever_evento_view(request: HttpRequest, pk: int):
    evento = get_object_or_404(Evento, id=pk)

    if not hasattr(request.user, "usuario"):
        messages.error(request, "Você precisa completar seu perfil de usuário.")
        return redirect("lista-eventos")

    if request.user.usuario.tipo == UsuarioTipo.ORGANIZADOR:
        messages.error(request, "Organizadores não podem se inscrever em eventos.")
        return redirect("lista-eventos")

    Inscricao.objects.filter(usuario=request.user.usuario, evento=evento).delete()

    evento.participantes -= 1
    evento.save()

    messages.success(
        request, f"Inscrição do evento {evento.nome} cancelada com sucesso!"
    )

    return redirect("lista-inscricoes")


@login_required
def inscricoes_lista_view(request: HttpRequest):

    if not hasattr(request.user, "usuario"):
        messages.error(request, "Você precisa completar seu perfil de usuário.")
        return redirect("lista-eventos")

    if request.user.usuario.tipo == UsuarioTipo.ORGANIZADOR:
        messages.error(request, "Organizadores não podem se inscrever em eventos.")
        return redirect("pagina-inicial")

    eventos = [x.evento for x in Inscricao.objects.filter(usuario=request.user.usuario)]

    return render(
        request,
        "lista_inscricoes.html",
        context={"eventos": eventos, "user": request.user},
    )


@login_required
def emitir_certificado_view(request):
    if (
        not hasattr(request.user, "usuario")
        or request.user.usuario.tipo != UsuarioTipo.ORGANIZADOR
    ):
        messages.error(request, "Apenas organizadores podem emitir certificados.")
        return redirect("pagina-inicial")

    if request.method == "POST":
        form = CertificadoForm(request.POST, organizador=request.user.usuario)

        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            evento = form.cleaned_data["evento"]

            try:
                inscricao = Inscricao.objects.get(usuario=usuario, evento=evento)
            except Inscricao.DoesNotExist:
                messages.error(
                    request,
                    f"{usuario.nome} não está inscrito no evento {evento.nome}.",
                )
                return render(request, "certificado_form.html", {"form": form})

            if Certificado.objects.filter(usuario=usuario, evento=evento).exists():
                messages.error(
                    request, f"{usuario.nome} já possui certificado para este evento."
                )
                return render(request, "certificado_form.html", {"form": form})

            certificado = form.save(commit=False)

            inscricao.delete()

            messages.success(
                request,
                f"Certificado emitido para {certificado.usuario.nome} com sucesso!",
            )
            return redirect("pagina-inicial")
        else:
            print(form.errors)
            messages.error(request, "Erro ao emitir certificado. Verifique os dados.")
    else:
        form = CertificadoForm(organizador=request.user.usuario)

    return render(request, "certificado_form.html", {"form": form})


@require_http_methods(["GET"])
@login_required
def get_usuarios_de_evento(request):
    evento_id = request.GET.get("evento_id")

    if not evento_id:
        return JsonResponse({"usuarios": []})

    evento = Evento.objects.filter(
        id=evento_id, organizador=request.user.usuario
    ).first()

    if not evento:
        return JsonResponse({"error": "Evento não encontrado"}, status=404)

    usuarios = Usuario.objects.filter(inscricao__evento=evento)
    dados_usuarios = [
        {"id": u.pk, "nome": f"{u.nome} ({u.instituicao})"} for u in usuarios
    ]

    return JsonResponse({"usuarios": dados_usuarios})


@require_http_methods(["GET"])
@login_required
def lista_certificados_view(request: HttpRequest):
    if not hasattr(request.user, "usuario"):
        messages.error(request, "Você precisa completar seu perfil de usuário.")
        return redirect("lista-certificados")

    if request.user.usuario == UsuarioTipo.ORGANIZADOR:
        messages.error(request, "Apenas alunos/professores podem ter certificados.")
        return redirect("pagina-inicial")

    certificados = list(Certificado.objects.filter(usuario=request.user.usuario))

    return render(
        request, "lista_certificados.html", context={"certificados": certificados}
    )


@require_http_methods(["GET"])
@login_required
def pagina_inicial_view(request):
    pagina_inicial = loader.get_template("pagina_inicial.html")
    return HttpResponse(pagina_inicial.render(context={"user": request.user}))
