from django.urls import path
from .views import home, cadastro, processar_cadastro, login_usuario, logout_usuario, lista_alunos
from . import views

urlpatterns = [
    path('', home, name='home'),  
    path('cadastro/', cadastro, name='cadastro'),
    path('processar_cadastro/', processar_cadastro, name="processar_cadastro"),
    path("login/", login_usuario, name="login"),
    path('logout/', logout_usuario, name='logout'),
     path('alunos/', lista_alunos, name='lista_alunos'),
    path('formulario/', views.formulario, name='formulario'),  
]