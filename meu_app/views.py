from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Perfil, Aluno
from .forms import FiltroAlunoForm

def home(request):
    return render(request, 'home.html', {
        'is_authenticated': request.user.is_authenticated  
    })

def cadastro(request):
    return render(request, 'cadastro.html')

def processar_cadastro(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        celular = request.POST.get("celular")
        data_nascimento = request.POST.get("data-nascimento")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse E-mail.")
            return render(request, "cadastro.html", {
                'nome': nome,
                'email': email,
                'cpf': cpf,
                'celular': celular,
                'data_nascimento': data_nascimento,
            })

        if Perfil.objects.filter(cpf=cpf).exists(): 
            messages.error(request, "Já existe um usuário cadastrado com esse CPF.")
            return render(request, "cadastro.html", {
                'nome': nome,
                'email': email,
                'cpf': cpf,
                'celular': celular,
                'data_nascimento': data_nascimento,
            })

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

    return render(request, "login.html", {'email': request.POST.get('email')})

def logout_usuario(request):
    logout(request)
    return redirect('home')

def lista_alunos(request):
    form = FiltroAlunoForm(request.GET or None)
    alunos = Aluno.objects.all()

    if form.is_valid():
        if form.cleaned_data.get('nome'):
            alunos = alunos.filter(nome__icontains=form.cleaned_data['nome'])
        if form.cleaned_data.get('email'):
            alunos = alunos.filter(email__icontains=form.cleaned_data['email'])
        if form.cleaned_data.get('serie'):
            alunos = alunos.filter(serie__icontains=form.cleaned_data['serie'])
        if form.cleaned_data.get('data_inscricao'):
            alunos = alunos.filter(data_inscricao__date=form.cleaned_data['data_inscricao'])

    return render(request, 'Lista_alunos.html', {'form': form, 'alunos': alunos})

def formulario(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para acessar o formulário.")
        return redirect('login')  

    return render(request, 'formulario.html')