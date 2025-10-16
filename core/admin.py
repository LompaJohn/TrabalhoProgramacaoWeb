from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import Usuario


class UsuarioInline(admin.StackedInline):
    model = Usuario
    fields = ("nome", "telefone", "instituicao", "perfil", "tipo")
    can_delete = False
    verbose_name_plural = "usuarios"


class UserAdmin(BaseUserAdmin):
    inlines = [UsuarioInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
