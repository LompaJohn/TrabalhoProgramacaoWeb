"""
URL configuration for SGEA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from lista_eventos.views import (
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    desinscrever_evento_view,
    emitir_certificado_view,
    get_usuarios_de_evento,
    inscrever_evento_view,
    inscricoes_lista_view,
    pagina_inicial_view,
    lista_certificados_view,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", pagina_inicial_view, name="pagina-inicial"),
    path("eventos/", EventoListView.as_view(), name="lista-eventos"),
    path("inscricoes/", inscricoes_lista_view, name="lista-inscricoes"),
    path("eventos/novo/", EventoCreateView.as_view(), name="criar-evento"),
    path("eventos/<int:pk>/inscrever", inscrever_evento_view, name="inscrever-evento"),
    path(
        "inscricoes/<int:pk>/desinscrever",
        desinscrever_evento_view,
        name="desinscrever-evento",
    ),
    path("certificados/", lista_certificados_view, name="lista-certificados"),
    path("certificados/emitir", emitir_certificado_view, name="emitir-certificado"),
    path("eventos/<int:pk>/editar", EventoUpdateView.as_view(), name="editar-evento"),
    path(
        "ajax/get_usuarios_evento",
        get_usuarios_de_evento,
        name="get-usuarios-de-evento",
    ),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
]
