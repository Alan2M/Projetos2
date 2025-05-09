from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('cadastro/', views.cadastro, name='cadastro'),
    path('processar_cadastro/', views.processar_cadastro, name="processar_cadastro"),
    path('login/', views.login_usuario, name="login"),
    path('logout/', views.logout_usuario, name='logout'),

    # Formulário de vulnerabilidade
    path("formulario/", views.formulario_view, name="formulario"),
    path('formulario/sucesso/', views.formulario_sucesso, name='formulario_sucesso'),

    # Rotas do gestor
    path('gestor/', views.painel_gestor, name='painel_gestor'),
    path('gestor/inicio/', views.inicio_gestor, name='inicio_gestor'),
    path('gestor/alunos/', views.lista_alunos, name='lista_alunos'),
    path('gestor/calendario/', views.calendario_entrevistas, name='calendario_entrevistas'),

    path('gestor/agendar/', views.agendar_entrevistas, name='agendar_entrevistas'),
    path('gestor/sucesso/', views.sucesso_agendamento, name='sucesso_agendamento'),
    path('entrevistas/', views.lista_entrevistas_por_dia, name='lista_entrevistas_por_dia'),
    path('entrevistas/', views.lista_entrevistas_por_dia, name='lista_entrevistas_por_dia'),
    path('entrevistas/editar/<int:pk>/', views.editar_entrevista, name='editar_entrevista'),
    path('entrevistas/excluir/<int:pk>/', views.excluir_entrevista, name='excluir_entrevista'),
    path('gestor/agendar-entrevista/', views.agendar_entrevista_individual, name='agendar_entrevista'),


    # Cadastro de alunos
    path('alunos/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
]
