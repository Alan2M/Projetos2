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

    # Cadastro de alunos
    path('alunos/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
]
