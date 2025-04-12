from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def processar_cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        cpf = request.POST.get("cpf")  

        if Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse CPF.")
            return render(request, "cadastro.html")

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse E-mail.")
            return render(request, "cadastro.html")

        usuario = Usuario(nome=nome, email=email, cpf=cpf)
        usuario.set_senha(senha)  
        usuario.save()

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("home")

    return render(request, "cadastro.html")

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            usuario = Usuario.objects.get(email=email) 
            if usuario.verificar_senha(senha): 
                messages.success(request, "Login realizado com sucesso!")
                return redirect("home")  
            else:
                messages.error(request, "Senha incorreta!")  
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado!")  

    return render(request, "login.html") 