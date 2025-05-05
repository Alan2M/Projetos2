from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Perfil, Aluno, FormularioMarcacao
from .forms import FiltroAlunoForm
from datetime import datetime

def home(request):
    return render(request, 'home.html', {
        'now': datetime.now(),
        'is_authenticated': request.user.is_authenticated
    })

def cadastro(request):
    return render(request, 'cadastro.html')

@login_required
def formulario_sucesso(request):
    return render(request, "formulario_sucesso.html")

def processar_cadastro(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar-senha")
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        celular = request.POST.get("celular")
        data_nascimento = request.POST.get("data-nascimento")
        tipo = request.POST.get("tipo")

        context = {
            'nome': nome,
            'email': email,
            'cpf': cpf,
            'celular': celular,
            'data_nascimento': data_nascimento,
            'tipo': tipo,
        }

        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "cadastro.html", context)

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse E-mail.")
            return render(request, "cadastro.html", context)

        if Perfil.objects.filter(cpf=cpf).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse CPF.")
            return render(request, "cadastro.html", context)

        try:
            data_nascimento_obj = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Data de nascimento inválida.")
            return render(request, "cadastro.html", context)

        usuario = User.objects.create_user(username=email, email=email, password=senha)

        if not hasattr(usuario, 'perfil'):
            usuario.perfil = Perfil.objects.create(
            user=usuario,
            nome=nome,
            cpf=cpf,
            celular=celular,
            data_nascimento=data_nascimento_obj,
            tipo=tipo,
            )
            usuario.save()

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("home")

    return render(request, "cadastro.html")

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        tipo = request.POST.get("tipo")  

        user = User.objects.filter(username=email).first()

        if user and user.check_password(senha):
            perfil = getattr(user, 'perfil', None)
            if perfil and perfil.tipo == tipo:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")

                if tipo == 'professor':
                    return redirect("lista_alunos")
                else:
                    return redirect("home")
            else:
                messages.error(request, "Tipo de login inválido para esse usuário.")
        else:
            messages.error(request, "Email ou senha incorretos!")

    return render(request, "login.html", {'email': request.POST.get('email')})

def logout_usuario(request):
    logout(request)
    return redirect('home')

def formulario(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para acessar o formulário.")
        return redirect('login')  
    return render(request, 'formulario.html')

from django.contrib.auth.decorators import login_required

@login_required
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

def formulario_view(request):
    try:
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(user=request.user)

    if perfil.score_vulnerabilidade > 0:
        formulario = FormularioMarcacao.objects.get(usuario=request.user)
        return render(request, "formulario_sucesso.html", {"formulario": formulario})

    if request.method == "POST":
        campos = [
            "pessoas_moram", "casa", "localizacao",
            "escolaridade_pai", "escolaridade_mae",
            "renda_familiar", "renda_mensal", "trabalha"
        ]

        respostas = {campo: request.POST.get(campo) for campo in campos}

        campos_vazios = [campo for campo, valor in respostas.items() if not valor]

        if campos_vazios:
            messages.error(request, "Por favor, preencha todas as respostas antes de enviar o formulário.")
            return render(request, "formulario.html", {"respostas": respostas})

        def calcular_score(respostas):
            score = 0
            if respostas["pessoas_moram"] == "Mais de dez":
                score += 3
            elif respostas["pessoas_moram"] == "Oito a dez":
                score += 2
            elif respostas["pessoas_moram"] == "Quatro a sete":
                score += 1

            if respostas["casa"] == "Cedida" or respostas["casa"] == "Outros":
                score += 2

            if respostas["localizacao"] in ["Zona rural", "Comunidade indígena", "Comunidade quilombola"]:
                score += 2

            if respostas["escolaridade_pai"] in ["Não estudou", "Não sei"]:
                score += 1

            if respostas["escolaridade_mae"] in ["Não estudou", "Não sei"]:
                score += 1

            if respostas["renda_familiar"] == "Nenhuma renda":
                score += 4
            elif respostas["renda_familiar"] == "Até 1 salário mínimo":
                score += 3
            elif respostas["renda_familiar"] == "De 1 a 3 salários mínimos":
                score += 2

            if respostas["renda_mensal"] == "Nenhuma renda":
                score += 2
            elif respostas["renda_mensal"] == "Até 1 salário mínimo":
                score += 1

            if respostas["trabalha"] == "Não":
                score += 1

            return score

        formulario = FormularioMarcacao.objects.create(
            usuario=request.user,
            pessoas_moram=respostas["pessoas_moram"],
            casa=respostas["casa"],
            localizacao=respostas["localizacao"],
            escolaridade_pai=respostas["escolaridade_pai"],
            escolaridade_mae=respostas["escolaridade_mae"],
            renda_familiar=respostas["renda_familiar"],
            renda_mensal=respostas["renda_mensal"],
            trabalha=respostas["trabalha"],
            score=calcular_score(respostas)
        )

        perfil.score_vulnerabilidade = formulario.score
        perfil.save()

        messages.success(request, "Formulário enviado com sucesso!")

        return render(request, "formulario_sucesso.html", {"formulario": formulario})

    formulario = FormularioMarcacao.objects.filter(usuario=request.user).first()
    if formulario:
        respostas = {
            "pessoas_moram": formulario.pessoas_moram,
            "casa": formulario.casa,
            "localizacao": formulario.localizacao,
            "escolaridade_pai": formulario.escolaridade_pai,
            "escolaridade_mae": formulario.escolaridade_mae,
            "renda_familiar": formulario.renda_familiar,
            "renda_mensal": formulario.renda_mensal,
            "trabalha": formulario.trabalha
        }
        return render(request, "formulario.html", {"respostas": respostas})

    return render(request, "formulario.html")

def processar_cadastro(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar-senha")
        cpf = request.POST.get("cpf")
        nome = request.POST.get("nome")
        celular = request.POST.get("celular")
        data_nascimento = request.POST.get("data-nascimento")
        tipo = request.POST.get("tipo")

        context = {
            'nome': nome,
            'email': email,
            'cpf': cpf,
            'celular': celular,
            'data_nascimento': data_nascimento,
            'tipo': tipo,
        }

        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "cadastro.html", context)

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse E-mail.")
            return render(request, "cadastro.html", context)

        if Perfil.objects.filter(cpf=cpf).exists():
            messages.error(request, "Já existe um usuário cadastrado com esse CPF.")
            return render(request, "cadastro.html", context)

        try:
            data_nascimento_obj = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Data de nascimento inválida.")
            return render(request, "cadastro.html", context)

        try:
            usuario = User.objects.create_user(username=email, email=email, password=senha)

            if not hasattr(usuario, 'perfil'):
                usuario.perfil = Perfil.objects.create(
                    user=usuario,
                    nome=nome,
                    cpf=cpf,
                    celular=celular,
                    data_nascimento=data_nascimento_obj,
                    tipo=tipo,
                )
                usuario.save()

            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("home")

        except Exception as e:
            print("Erro ao criar usuário ou perfil:", e)  # Mostra no terminal/log do Azure
            messages.error(request, f"Ocorreu um erro interno ao cadastrar: {str(e)}")
            return render(request, "cadastro.html", context)

    return render(request, "cadastro.html")