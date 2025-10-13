from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsuarioTipo(models.TextChoices):
    PROFESSOR = "PF", _("professor")
    ALUNO = "AL", _("aluno")
    ORGANIZADOR = "OR", _("organizador")


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255, unique=True)
    instituicao = models.CharField(max_length=255, null=True)
    perfil = models.CharField()  # ?
    tipo = models.CharField(max_length=2, choices=UsuarioTipo.choices)
    data_cadastro = models.DateTimeField(auto_now_add=True)


class EventoTipo(models.TextChoices):
    SEMINARIO = "SE", _("seminário")
    PALESTRA = "PL", _("palestra")


def validar_organizador(usuario: Usuario):
    if usuario.tipo != UsuarioTipo.ORGANIZADOR:
        raise ValidationError(
            _("usuário '%(usuario)s' não eh um organizador"),
            params={"usuario": usuario.user.username},
        )


class Evento(models.Model):
    tipo = models.CharField(max_length=2, choices=EventoTipo.choices)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    local = models.CharField(max_length=255)
    participantes = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
    organizador = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        validators=[
            validar_organizador,
        ],
    )


class Inscricao(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
    )
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
    )
    data_inscricao = models.DateTimeField(auto_now_add=True)


class Certificado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    data_emissao = models.DateTimeField(auto_now_add=True)
