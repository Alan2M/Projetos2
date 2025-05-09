from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from .models import Perfil, Aluno, FormularioMarcacao
from .forms import FiltroAlunoForm, AlunoForm, CriarAdministradorForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import AgendamentoForm
from .models import Aluno, Entrevista
from datetime import datetime, timedelta
from .forms import EntrevistaForm
from datetime import time


# ---------- AUTENTICAÇÃO ----------

def home(request):
    return render(request, 'home.html', {
        'now': datetime.now(),
        'is_authenticated': request.user.is_authenticated
    })



def cadastro(request):
    return render(request, 'cadastro.html')

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
            'nome': nome, 'email': email, 'cpf': cpf,
            'celular': celular, 'data_nascimento': data_nascimento,
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
            Perfil.objects.create(
                user=usuario,
                nome=nome,
                cpf=cpf,
                celular=celular,
                data_nascimento=data_nascimento_obj,
                tipo=tipo,
            )
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("home")

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar: {str(e)}")
            return render(request, "cadastro.html", context)

    return render(request, "cadastro.html")

def is_professor(user):
    return user.is_authenticated and user.perfil.tipo == 'professor'

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
                return redirect("inicio_gestor") if tipo == 'professor' else redirect("home")
            else:
                messages.error(request, "Tipo de login inválido para esse usuário.")
        else:
            messages.error(request, "Email ou senha incorretos!")

    return render(request, "login.html", {'email': request.POST.get('email')})

def logout_usuario(request):
    logout(request)
    return redirect('home')



# ---------- FORMULÁRIOS E PERFIL ----------

@login_required
def formulario(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para acessar o formulário.")
        return redirect('login')
    return render(request, 'formulario.html')

@login_required
def formulario_view(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    if perfil.score_vulnerabilidade > 0:
        formulario = FormularioMarcacao.objects.filter(usuario=request.user).first()
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
            messages.error(request, "Por favor, preencha todas as respostas.")
            return render(request, "formulario.html", {"respostas": respostas})

        def calcular_score(r):
            score = 0
            if r["pessoas_moram"] == "Mais de dez": score += 3
            elif r["pessoas_moram"] == "Oito a dez": score += 2
            elif r["pessoas_moram"] == "Quatro a sete": score += 1
            if r["casa"] in ["Cedida", "Outros"]: score += 2
            if r["localizacao"] in ["Zona rural", "Comunidade indígena", "Comunidade quilombola"]: score += 2
            if r["escolaridade_pai"] in ["Não estudou", "Não sei"]: score += 1
            if r["escolaridade_mae"] in ["Não estudou", "Não sei"]: score += 1
            if r["renda_familiar"] == "Nenhuma renda": score += 4
            elif r["renda_familiar"] == "Até 1 salário mínimo": score += 3
            elif r["renda_familiar"] == "De 1 a 3 salários mínimos": score += 2
            if r["renda_mensal"] == "Nenhuma renda": score += 2
            elif r["renda_mensal"] == "Até 1 salário mínimo": score += 1
            if r["trabalha"] == "Não": score += 1
            return score

        score = calcular_score(respostas)
        FormularioMarcacao.objects.create(usuario=request.user, score=score, **respostas)
        perfil.score_vulnerabilidade = score
        perfil.save()
        messages.success(request, "Formulário enviado com sucesso!")
        return render(request, "formulario_sucesso.html", {"formulario": respostas})

    return render(request, "formulario.html")

@login_required
def formulario_sucesso(request):
    return render(request, "formulario_sucesso.html")

# ---------- PAINEL E GESTÃO ----------

<<<<<<< Updated upstream
@user_passes_test(is_professor)
=======
from .models import Curso 
@login_required
>>>>>>> Stashed changes
def painel_gestor(request):
    form = FiltroAlunoForm(request.GET or None)
    alunos = Aluno.objects.all()

    if form.is_valid():
        if form.cleaned_data.get('nome'):
            alunos = alunos.filter(nome__icontains=form.cleaned_data['nome'])
        if form.cleaned_data.get('email'):
            alunos = alunos.filter(email__icontains=form.cleaned_data['email'])
        if form.cleaned_data.get('data_inscricao'):
            alunos = alunos.filter(data_inscricao__date=form.cleaned_data['data_inscricao'])
        if form.cleaned_data.get('curso'):
            alunos = alunos.filter(curso=form.cleaned_data['curso'])

    return render(request, 'gestor.html', {
        'alunos': alunos,
        'form': form,
        'cursos': Curso.objects.all(),  
    })


@user_passes_test(is_professor)
def lista_alunos(request):
    form = FiltroAlunoForm(request.GET or None)
    perfis = Perfil.objects.filter(tipo='aluno').select_related('user')
    
    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        email = form.cleaned_data.get('email')
        cpf = form.cleaned_data.get('cpf')
        data_inscricao = form.cleaned_data.get('data_inscricao')

        if nome:
            perfis = perfis.filter(nome__icontains=nome)
        if email:
            perfis = perfis.filter(user__email__icontains=email)
        if cpf:
            perfis = perfis.filter(cpf__icontains=cpf)
        if data_inscricao:
            perfis = perfis.filter(user__date_joined__date=data_inscricao)

    # Ordenação por score
    ordenar_score = request.GET.get('ordenar_score')
    if ordenar_score == 'asc':
        perfis = perfis.order_by('score_vulnerabilidade')
    elif ordenar_score == 'desc':
        perfis = perfis.order_by('-score_vulnerabilidade')

    return render(request, 'lista_alunos.html', {
        'form': form,
        'alunos': perfis
    })

@login_required
def cadastrar_aluno(request):
    nome = request.GET.get('nome')
    email = request.GET.get('email')
    curso_nome = request.GET.get('curso')

    dados_iniciais = {
        'nome': nome or '',
        'email': email or '',
    }

    if curso_nome:
        try:
            curso = Curso.objects.get(nome=curso_nome)
            dados_iniciais['curso'] = curso
        except Curso.DoesNotExist:
            pass

    perfil = None
    if nome and email:
        perfil = Perfil.objects.filter(nome=nome, user__email=email).first()

    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Aluno.objects.filter(email=email).exists():
                messages.error(request, "Já existe um aluno cadastrado com esse e-mail.")
            else:
                form.save()

                if perfil:
                    user = perfil.user
                    perfil.delete()
                    user.delete()

                messages.success(request, "Aluno cadastrado com sucesso!")
                return redirect('painel_gestor')
    else:
        form = AlunoForm(initial=dados_iniciais)

    return render(request, 'cadastrar_aluno.html', {'form': form, 'perfil': perfil})

@login_required
def inicio_gestor(request):
    total_alunos = Aluno.objects.count()
    total_formularios = FormularioMarcacao.objects.count()
    form = CriarAdministradorForm()

    if request.method == "POST":
        form = CriarAdministradorForm(request.POST)
        if form.is_valid():
            novo_admin = form.save(commit=False)
            novo_admin.set_password(form.cleaned_data['senha'])
            novo_admin.save()
            Perfil.objects.create(
                user=novo_admin,
                nome=novo_admin.username,
                tipo='professor',
                data_nascimento='2000-01-01'
            )
            messages.success(request, "Administrador criado com sucesso!")

    return render(request, 'inicio_gestor.html', {
        'total_alunos': total_alunos,
        'total_formularios': total_formularios,
        'form': form
    })

from django.shortcuts import render
from .models import Aluno
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
import calendar

@login_required
def calendario_entrevistas(request):
    hoje = date.today()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    cal = calendar.Calendar(firstweekday=6)  # domingo primeiro
    semanas = cal.monthdatescalendar(ano, mes)

    # Exemplo de eventos fictícios (substitua por dados reais do banco)
    eventos = {
        '2025-01-17': ['Entrevista com João'],
        '2025-01-23': ['Entrevista com Maria'],
    }

    contexto = {
        'ano': ano,
        'mes': mes,
        'semanas': semanas,
        'eventos': eventos,
        'nome_mes': calendar.month_name[mes],
        'anterior': {'mes': mes - 1 or 12, 'ano': ano - 1 if mes == 1 else ano},
        'proximo': {'mes': mes + 1 if mes < 12 else 1, 'ano': ano + 1 if mes == 12 else ano},
    }

    return render(request, 'calendario.html', contexto)

def agendar_entrevistas(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            curso = form.cleaned_data['curso']
            qtd = form.cleaned_data['quantidade_alunos']
            periodo = form.cleaned_data['periodo']
            dia = form.cleaned_data['dia_agendamento']

            # Horários fixos com base no período
            if periodo == 'manha':
                hora_inicial = time(hour=8)
                hora_final = time(hour=11)
            else:  # tarde
                hora_inicial = time(hour=13)
                hora_final = time(hour=16)

            # Gera lista de horários a cada 30 min
            horarios = []
            atual = datetime.combine(dia, hora_inicial)
            fim = datetime.combine(dia, hora_final)
            while atual <= fim and len(horarios) < qtd:
                horarios.append(atual)
                atual += timedelta(minutes=30)

            # Pega os alunos com maior score
            alunos = Aluno.objects.filter(curso=curso).order_by('-score')[:len(horarios)]

            for aluno, horario in zip(alunos, horarios):
                entrevista = Entrevista.objects.create(
                    aluno=aluno,
                    curso=curso,
                    data_hora=horario,
                    local="R. Alcântara, 170 - Coqueiral, Recife - PE, 50791-560"
                )

                aluno.data_entrevista = horario
                aluno.save()

                send_mail(
                    subject='Entrevista Agendada',
                    message=f"""
Olá {aluno.nome},

Você foi selecionado para uma entrevista do curso "{curso.nome}".

🗓 Data: {horario.strftime('%d/%m/%Y')}
🕒 Hora: {horario.strftime('%H:%M')}
📍 Local: R. Alcântara, 170 - Coqueiral, Recife - PE, 50791-560

Compareça com 10 minutos de antecedência. Boa sorte!

Atenciosamente,
Equipe de Seleção
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[aluno.email],
                    fail_silently=False
                )

            return redirect('sucesso_agendamento')
    else:
        form = AgendamentoForm()

    return render(request, 'agendar_entrevistas.html', {'form': form})

from .models import Entrevista

@login_required
def lista_entrevistas_por_dia(request):
    data_str = request.GET.get('data')
    entrevistas = []

    if data_str:
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            entrevistas = Entrevista.objects.filter(data_hora__date=data)
        except ValueError:
            messages.error(request, "Data inválida.")

    return render(request, 'entrevistas_por_dia.html', {
        'data': data_str,
        'entrevistas': entrevistas
    })

eventos = {}
for entrevista in Entrevista.objects.all():
    data_str = entrevista.data_hora.strftime('%Y-%m-%d')
    eventos.setdefault(data_str, []).append(f"{entrevista.aluno.nome} - {entrevista.data_hora.strftime('%H:%M')}")

@login_required
def editar_entrevista(request, pk):
    entrevista = get_object_or_404(Entrevista, pk=pk)
    if request.method == 'POST':
        form = EntrevistaForm(request.POST, instance=entrevista)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrevista atualizada com sucesso!")
            return redirect('lista_entrevistas_por_dia')  # você pode passar ?data=... de volta se quiser
    else:
        form = EntrevistaForm(instance=entrevista)
    return render(request, 'editar_entrevista.html', {'form': form})

@login_required
def excluir_entrevista(request, pk):
    entrevista = get_object_or_404(Entrevista, pk=pk)
    entrevista.delete()
    messages.success(request, "Entrevista excluída com sucesso!")
    return redirect('calendario_entrevistas')

@login_required
def sucesso_agendamento(request):
    return render(request, 'sucesso.html')

@login_required
def agendar_entrevista_individual(request):
    aluno_id = request.GET.get('aluno_id')
    aluno = get_object_or_404(Aluno, id=aluno_id) if aluno_id else None

    if request.method == 'POST':
        form = EntrevistaForm(request.POST)
        if form.is_valid():
            entrevista = form.save()
            aluno.data_entrevista = entrevista.data_hora
            aluno.save()
            messages.success(request, "Entrevista agendada com sucesso.")
            return redirect('painel_gestor')
    else:
        form = EntrevistaForm(initial={'aluno': aluno})

    return render(request, 'agendar_entrevistas.html', {
        'form': form,
        'aluno_selecionado': aluno
    })