from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home, cadastro, processar_cadastro, login_usuario

urlpatterns = [
    path('', home, name='home'),  
    path('cadastro/', cadastro, name='cadastro'),
    path('processar_cadastro/', processar_cadastro, name="processar_cadastro"),
    path("login/", login_usuario, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]