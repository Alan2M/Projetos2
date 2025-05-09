from django.urls import path
from . import views

urlpatterns = [
    # — Rotas públicas —
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('processar_cadastro/', views.processar_cadastro, name='processar_cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('formulario/', views.formulario_view, name='formulario'),
    path('formulario/sucesso/', views.formulario_sucesso, name='formulario_sucesso'),

    # — Painel do gestor —
    path('gestor/', views.painel_gestor, name='painel_gestor'),
    path('gestor/inicio/', views.inicio_gestor, name='inicio_gestor'),
    path('gestor/alunos/', views.lista_alunos, name='lista_alunos'),
    path('gestor/calendario/', views.calendario_entrevistas, name='calendario_entrevistas'),

    # — Agendamento de entrevistas em lote —
    path('gestor/agendar-vagas/', views.agendar_vagas, name='agendar_vagas'),

    # — Agendamento de entrevista individual —
    path('gestor/agendar-entrevista/', views.agendar_entrevista_individual, name='agendar_entrevista'),

    # — CRUD de entrevistas dentro do gestor —
    path('gestor/entrevistas/', views.lista_entrevistas_por_dia, name='lista_entrevistas_por_dia'),
    path('gestor/entrevistas/editar/<int:pk>/', views.editar_entrevista, name='editar_entrevista'),
    path('gestor/entrevistas/excluir/<int:pk>/', views.excluir_entrevista, name='excluir_entrevista'),

    # — FILTRAR entrevistas por curso —
    path(
        'gestor/entrevistas/curso/<int:curso_id>/',
        views.lista_entrevistas_por_curso,
        name='lista_entrevistas_por_curso'
    ),

    # — Listar todas as entrevistas —
    path(
        'gestor/entrevistas/todas/',
        views.todas_entrevistas,
        name='todas_entrevistas'
    ),

    # — Cadastro de alunos —
    path('alunos/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
]
