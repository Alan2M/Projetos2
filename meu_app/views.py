from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Perfil  

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def processar_cadastro(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        cpf = request.POST.get("cpf")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse E-mail.")
            return render(request, "cadastro.html")

        if User.objects.filter(perfil__cpf=cpf).exists(): 
            messages.error(request, "Já existe um usuário cadastrado com esse CPF.")
            return render(request, "cadastro.html")

        usuario = User.objects.create_user(username=email, email=email, password=senha)
        
        if not hasattr(usuario, 'perfil'):  
            usuario.perfil = Perfil.objects.create(user=usuario, cpf=cpf)
            usuario.save()

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("home")

    return render(request, "cadastro.html")

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = User.objects.filter(username=email).first()  

        if user and user.check_password(senha):  
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Email ou senha incorretos!")

    return render(request, "login.html")

def logout_usuario(request):
    logout(request)
    return redirect('home')