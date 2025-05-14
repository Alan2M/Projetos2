from datetime import datetime, date, time, timedelta
import calendar

from django.shortcuts            import render, redirect, get_object_or_404
from django.contrib               import messages
from django.contrib.auth          import authenticate, login, logout
from django.contrib.auth.models   import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail             import send_mail
from django.conf                  import settings
from django import forms
from django.db                    import IntegrityError

from .models import (
    Perfil, Aluno, FormularioMarcacao, Curso, Entrevista
)
from .forms import (
    FiltroAlunoForm, AlunoForm, CriarAdministradorForm,
    AgendamentoForm, EntrevistaForm
)


# -----------------------------------------------------------
#  Helpers
# -----------------------------------------------------------

def is_professor(user):
    """Retorna True se o usuário for superuser ou perfil.tipo == 'professor'."""
    return (
        user.is_authenticated and (
            user.is_superuser or
            (hasattr(user, 'perfil') and user.perfil.tipo == 'professor')
        )
    )


# -----------------------------------------------------------
#  Páginas públicas / autenticação
# -----------------------------------------------------------

def home(request):
    return render(request, "home.html", {
        "now": datetime.now(),
        "is_authenticated": request.user.is_authenticated,
    })


def cadastro(request):
    return render(request, "cadastro.html", {"cursos": Curso.objects.all()})


def processar_cadastro(request):
    if request.method != "POST":
        return redirect("cadastro")

    email            = request.POST.get("email")
    senha            = request.POST.get("senha")
    confirmar_senha  = request.POST.get("confirmar-senha")
    cpf              = request.POST.get("cpf")
    nome             = request.POST.get("nome")
    celular          = request.POST.get("celular")
    data_nascimento  = request.POST.get("data-nascimento")
    curso_id         = request.POST.get("curso")

    context = {
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "celular": celular,
        "data_nascimento": data_nascimento,
        "cursos": Curso.objects.all(),
        "curso_selecionado": curso_id,
    }

    if senha != confirmar_senha:
        messages.error(request, "As senhas não coincidem.")
        return render(request, "cadastro.html", context)

    if User.objects.filter(username=email).exists():
        messages.error(request, "Já existe um usuário cadastrado com esse e‑mail.")
        return render(request, "cadastro.html", context)

    if Perfil.objects.filter(cpf=cpf).exists():
        messages.error(request, "Já existe um usuário cadastrado com esse CPF.")
        return render(request, "cadastro.html", context)

    try:
        data_nasc = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Data de nascimento inválida.")
        return render(request, "cadastro.html", context)

    try:
        usuario   = User.objects.create_user(username=email, email=email, password=senha)
        curso_obj = Curso.objects.filter(pk=curso_id).first() if curso_id else None

        Perfil.objects.create(
            user=usuario,
            nome=nome,
            cpf=cpf,
            celular=celular,
            data_nascimento=data_nasc,
            tipo="aluno",
            curso=curso_obj,
        )
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("home")

    except Exception as e:
        messages.error(request, f"Erro ao cadastrar: {e}")
        return render(request, "cadastro.html", context)


def login_usuario(request):
    if request.method == "POST":
        login_input = request.POST.get("email", "").strip()
        senha       = request.POST.get("senha", "").strip()

        user = authenticate(request, username=login_input, password=senha)

        if user is None:                           # tentar username == email
            try:
                by_email = User.objects.get(email=login_input)
                user = authenticate(request, username=by_email.username, password=senha)
            except User.DoesNotExist:
                pass

        if user is None:
            messages.error(request, "E‑mail ou senha incorretos!")
        else:
            perfil = getattr(user, "perfil", None)
            if perfil is None:
                messages.error(request, "Perfil de usuário não encontrado.")
            else:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")

                if user.is_superuser:
                    return redirect("inicio_gestor")
                if perfil.tipo == "professor":
                    return redirect("painel_gestor")
                return redirect("home")

    return render(request, "login.html", {"email": request.POST.get("email", "")})


def logout_usuario(request):
    logout(request)
    return redirect("home")


# -----------------------------------------------------------
#  Formulário socioeconômico
# -----------------------------------------------------------

@login_required
def formulario_view(request):
    perfil, _ = Perfil.objects.get_or_create(
        user=request.user,
        defaults={
            "nome": request.user.username or request.user.email,
            "data_nascimento": date.today(),
            "tipo": "aluno",
        }
    )

    if perfil.score_vulnerabilidade > 0:
        formulario = FormularioMarcacao.objects.filter(usuario=request.user).first()
        return render(request, "formulario_sucesso.html", {"formulario": formulario})

    if request.method == "POST":
        campos = [
            "pessoas_moram", "casa", "localizacao",
            "escolaridade_pai", "escolaridade_mae",
            "renda_familiar", "renda_mensal", "trabalha"
        ]
        respostas = {c: request.POST.get(c) for c in campos}

        if any(not v for v in respostas.values()):
            messages.error(request, "Por favor, preencha todas as respostas.")
            return render(request, "formulario.html", {"respostas": respostas})

        def calc(r):
            s = 0
            if r["pessoas_moram"] == "Mais de dez": s += 3
            elif r["pessoas_moram"] == "Oito a dez": s += 2
            elif r["pessoas_moram"] == "Quatro a sete": s += 1
            if r["casa"] in ["Cedida", "Outros"]: s += 2
            if r["localizacao"] in ["Zona rural", "Comunidade indígena", "Comunidade quilombola"]: s += 2
            if r["escolaridade_pai"] in ["Não estudou", "Não sei"]: s += 1
            if r["escolaridade_mae"] in ["Não estudou", "Não sei"]: s += 1
            if r["renda_familiar"] == "Nenhuma renda": s += 4
            elif r["renda_familiar"] == "Até 1 salário mínimo": s += 3
            elif r["renda_familiar"] == "De 1 a 3 salários mínimos": s += 2
            if r["renda_mensal"] == "Nenhuma renda": s += 2
            elif r["renda_mensal"] == "Até 1 salário mínimo": s += 1
            if r["trabalha"] == "Não": s += 1
            return s

        score = calc(respostas)
        FormularioMarcacao.objects.create(usuario=request.user, score=score, **respostas)
        perfil.score_vulnerabilidade = score
        perfil.save()

        messages.success(request, "Formulário enviado com sucesso!")
        return render(request, "formulario_sucesso.html", {"formulario": respostas})

    return render(request, "formulario.html")


@login_required
def formulario_sucesso(request):
    return render(request, "formulario_sucesso.html")


# -----------------------------------------------------------
#  Painel do gestor (professor)
# -----------------------------------------------------------

@login_required
@user_passes_test(is_professor)
def painel_gestor(request):
    form   = FiltroAlunoForm(request.GET or None)
    alunos = Aluno.objects.all()

    if form.is_valid():
        if form.cleaned_data.get("nome"):
            alunos = alunos.filter(nome__icontains=form.cleaned_data["nome"])
        if form.cleaned_data.get("email"):
            alunos = alunos.filter(email__icontains=form.cleaned_data["email"])
        if form.cleaned_data.get("data_inscricao"):
            alunos = alunos.filter(data_inscricao__date=form.cleaned_data["data_inscricao"])
        if form.cleaned_data.get("curso"):
            alunos = alunos.filter(curso=form.cleaned_data["curso"])

    return render(
        request, "gestor.html",
        {"alunos": alunos, "form": form, "cursos": Curso.objects.all()}
    )


@login_required
@user_passes_test(is_professor)
def lista_alunos(request):
    form   = FiltroAlunoForm(request.GET or None)
    perfis = Perfil.objects.filter(tipo="aluno").select_related("user")

    if form.is_valid():
        if form.cleaned_data.get("nome"):
            perfis = perfis.filter(nome__icontains=form.cleaned_data["nome"])
        if form.cleaned_data.get("email"):
            perfis = perfis.filter(user__email__icontains=form.cleaned_data["email"])
        if form.cleaned_data.get("cpf"):
            perfis = perfis.filter(cpf__icontains=form.cleaned_data["cpf"])
        if form.cleaned_data.get("data_inscricao"):
            perfis = perfis.filter(user__date_joined__date=form.cleaned_data["data_inscricao"])

    ordenar_score = request.GET.get("ordenar_score")
    if ordenar_score == "asc":
        perfis = perfis.order_by("score_vulnerabilidade")
    elif ordenar_score == "desc":
        perfis = perfis.order_by("-score_vulnerabilidade")

    return render(request, "lista_alunos.html", {"form": form, "alunos": perfis})


@login_required
@user_passes_test(is_professor)
def cadastrar_aluno(request):
    nome       = request.GET.get("nome")
    email      = request.GET.get("email")
    curso_nome = request.GET.get("curso")

    iniciais = {"nome": nome or "", "email": email or ""}
    if curso_nome:
        iniciais["curso"] = Curso.objects.filter(nome=curso_nome).first()

    perfil_preexistente = (
        Perfil.objects.filter(nome=nome, user__email=email).first()
        if nome and email else None
    )

    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            if Aluno.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(request, "Já existe um aluno cadastrado com esse e‑mail.")
            else:
                aluno = form.save(commit=False)
                if perfil_preexistente:
                    aluno.cpf = perfil_preexistente.cpf
                aluno.save()

                if perfil_preexistente:
                    perfil_preexistente.user.delete()
                    perfil_preexistente.delete()

                messages.success(request, "Aluno cadastrado com sucesso!")
                return redirect("painel_gestor")
    else:
        form = AlunoForm(initial=iniciais)

    return render(request, "cadastrar_aluno.html", {"form": form, "perfil": perfil_preexistente})


# -----------------------------------------------------------
#  Dashboard (apenas superusuário) – criação de Gestores
# -----------------------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def inicio_gestor(request):
    total_alunos      = Aluno.objects.count()
    total_formularios = FormularioMarcacao.objects.count()

    context_inputs = {"username_val": "", "email_val": ""}

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email    = request.POST.get("email", "").strip()
        senha    = request.POST.get("senha", "").strip()

        context_inputs.update({"username_val": username, "email_val": email})

        if not username or not email or not senha:
            messages.error(request, "Todos os campos são obrigatórios.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já cadastrado.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário com este e‑mail.")
        elif len(senha) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
        else:
            try:
                novo_user = User.objects.create_user(username=username, email=email, password=senha)
                Perfil.objects.create(
                    user=novo_user,
                    nome=novo_user.username,
                    tipo="professor",
                    data_nascimento=date.today()
                )
                messages.success(request, "Gestor criado com sucesso!")
                return redirect("inicio_gestor")
            except IntegrityError:
                messages.error(request, "Erro ao criar usuário. Verifique se nome ou e‑mail já existem.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")

    return render(request, "inicio_gestor.html", {
        "total_alunos": total_alunos,
        "total_formularios": total_formularios,
        **context_inputs,
    })


# -----------------------------------------------------------
#  Entrevistas – calendário, agendamento, edição
# -----------------------------------------------------------

@login_required
@user_passes_test(is_professor)
def calendario_entrevistas(request):
    hoje = date.today()
    mes  = int(request.GET.get("mes", hoje.month))
    ano  = int(request.GET.get("ano", hoje.year))

    cal      = calendar.Calendar(firstweekday=6)
    semanas  = cal.monthdatescalendar(ano, mes)
    eventos  = {}

    entrevistas_mes = Entrevista.objects.filter(data_hora__year=ano, data_hora__month=mes)
    for e in entrevistas_mes:
        dia = e.data_hora.strftime("%Y-%m-%d")
        eventos.setdefault(dia, []).append(f"{e.aluno.nome} - {e.data_hora:%H:%M}")

    return render(request, "calendario.html", {
        "ano": ano,
        "mes": mes,
        "semanas": semanas,
        "eventos": eventos,
        "nome_mes": calendar.month_name[mes],
        "anterior": {"mes": mes - 1 or 12, "ano": ano - 1 if mes == 1 else ano},
        "proximo":  {"mes": mes + 1 if mes < 12 else 1, "ano": ano + 1 if mes == 12 else ano},
    })


@login_required
@user_passes_test(is_professor)
def agendar_vagas(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            curso = form.cleaned_data["curso"]
            qtd   = form.cleaned_data["quantidade_alunos"]
            periodo = form.cleaned_data["periodo"]
            dia     = form.cleaned_data["dia_agendamento"]

            inicio, fim = (time(8, 0), time(11, 0)) if periodo == "manha" else (time(13, 0), time(16, 0))

            slots, atual = [], datetime.combine(dia, inicio)
            while atual <= datetime.combine(dia, fim) and len(slots) < qtd:
                slots.append(atual)
                atual += timedelta(minutes=30)

            alunos = Aluno.objects.filter(curso=curso).order_by("-perfil__score_vulnerabilidade")[:len(slots)]

            for aluno, dt in zip(alunos, slots):
                Entrevista.objects.create(
                    aluno=aluno, curso=curso, data_hora=dt,
                    local="R. Alcântara, 170 - Coqueiral, Recife - PE"
                )
                aluno.data_entrevista = dt
                aluno.save()

                send_mail(
                    subject="Entrevista Agendada",
                    message=(
                        f"Olá {aluno.nome},\n\n"
                        f"Entrevista do curso \"{curso.nome}\" em {dt:%d/%m/%Y %H:%M}\n"
                        "no endereço acima.\n\nBoa sorte!"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[aluno.email],
                    fail_silently=False,
                )
            return redirect("sucesso_agendamento")
    else:
        form = AgendamentoForm()

    return render(request, "agendar_vagas.html", {"form": form})


@login_required
@user_passes_test(is_professor)
def lista_entrevistas_por_dia(request):
    data_str   = request.GET.get("data")
    entrevistas = []
    if data_str:
        try:
            dia         = datetime.strptime(data_str, "%Y-%m-%d").date()
            entrevistas = Entrevista.objects.filter(data_hora__date=dia)
        except ValueError:
            messages.error(request, "Data inválida.")

    return render(request, "entrevistas_por_dia.html",
                  {"data": data_str, "entrevistas": entrevistas})


@login_required
@user_passes_test(is_professor)
def editar_entrevista(request, pk):
    entrevista = get_object_or_404(Entrevista, pk=pk)

    if request.method == "POST":
        form = EntrevistaForm(request.POST, instance=entrevista)
        if form.is_valid():
            e = form.save(commit=False)
            e.aluno = entrevista.aluno
            e.curso = entrevista.curso
            e.save()
            messages.success(request, "Entrevista atualizada com sucesso!")
            return redirect("lista_entrevistas_por_dia")
    else:
        form = EntrevistaForm(instance=entrevista)
        form.fields["aluno"].widget  = forms.HiddenInput()
        form.fields["curso"].widget  = forms.HiddenInput()

    return render(request, "editar_entrevista.html", {"form": form, "entrevista": entrevista})


@login_required
@user_passes_test(is_professor)
def excluir_entrevista(request, pk):
    entrevista = get_object_or_404(Entrevista, pk=pk)
    entrevista.delete()
    messages.success(request, "Entrevista excluída com sucesso!")
    return redirect("calendario_entrevistas")


@login_required
@user_passes_test(is_professor)
def sucesso_agendamento(request):
    return render(request, "sucesso.html")


@login_required
@user_passes_test(is_professor)
def agendar_entrevista_individual(request):
    aluno_id = request.GET.get("aluno_id")
    aluno    = get_object_or_404(Aluno, id=aluno_id) if aluno_id else None

    if request.method == "POST":
        form = EntrevistaForm(request.POST)
        if form.is_valid():
            entrevista              = form.save()
            aluno.data_entrevista   = entrevista.data_hora
            aluno.save()
            messages.success(request, "Entrevista agendada com sucesso.")
            return redirect("painel_gestor")
    else:
        form = EntrevistaForm(initial={"aluno": aluno})

    return render(request, "agendar_entrevista.html", {"form": form, "aluno_selecionado": aluno})


@login_required
@user_passes_test(is_professor)
def lista_entrevistas_por_curso(request, curso_id):
    curso       = get_object_or_404(Curso, pk=curso_id)
    entrevistas = Entrevista.objects.filter(curso=curso)
    return render(request, "entrevistas_por_curso.html", {"curso": curso, "entrevistas": entrevistas})


@login_required
@user_passes_test(is_professor)
def todas_entrevistas(request):
    cursos      = Curso.objects.all().order_by("nome")
    curso_id    = request.GET.get("curso")
    entrevistas = Entrevista.objects.all().order_by("data_hora")
    if curso_id:
        entrevistas = entrevistas.filter(curso__id=curso_id)

    return render(request, "todas_entrevistas.html", {
        "cursos": cursos,
        "entrevistas": entrevistas,
        "curso_selecionado": int(curso_id) if curso_id else None,
    })


# -----------------------------------------------------------
#  Gestão de Gestores (superusuário)
# -----------------------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def lista_professores(request):
    profs = Perfil.objects.filter(tipo="professor").select_related("user")
    return render(request, "lista_professores.html", {"profs": profs})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_professor(request, user_id):
    prof_user = get_object_or_404(User, id=user_id)
    perfil    = prof_user.perfil

    if request.method == "POST":
        nome  = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "").strip()

        if not nome or not email:
            messages.error(request, "Nome e e‑mail são obrigatórios.")
        else:
            prof_user.email    = email
            prof_user.username = email      # username = e‑mail
            if senha:
                prof_user.set_password(senha)
            prof_user.save()

            perfil.nome = nome
            perfil.save()

            messages.success(request, "Gestor atualizado!")
            return redirect("lista_professores")

    return render(request, "editar_professor.html", {"prof": perfil})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def excluir_professor(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, "Gestor excluído.")
    return redirect("lista_professores")
