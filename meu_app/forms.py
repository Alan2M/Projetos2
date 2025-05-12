from django import forms
from django.contrib.auth.models import User
from .models import Aluno, Curso, Entrevista, FormularioMarcacao
from datetime import timedelta
from django.utils import timezone

# ---------------------------
# Choices de período/turno
# ---------------------------
PERIODO_CHOICES = [
    ('manha', 'Manhã'),
    ('tarde', 'Tarde'),
    ('noite', 'Noite'),
]

# ---------------------------
# Formulário de Inscrição (vulnerabilidade + curso/turno)
# ---------------------------
class FormularioMarcacaoForm(forms.ModelForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        label='Curso desejado',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    turno = forms.ChoiceField(
        choices=PERIODO_CHOICES,
        widget=forms.RadioSelect,
        label='Turno desejado'
    )

    class Meta:
        model = FormularioMarcacao
        fields = [
            'pessoas_moram', 'casa', 'localizacao',
            'escolaridade_pai', 'escolaridade_mae',
            'renda_familiar', 'renda_mensal', 'trabalha',
            'curso', 'turno'
        ]

# ---------------------------
# Filtro de Alunos no Painel
# ---------------------------
class FiltroAlunoForm(forms.Form):
    nome = forms.CharField(required=False, label='Nome')
    email = forms.CharField(required=False, label='Email')
    cpf = forms.CharField(required=False, label='CPF')
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.none(),
        required=False,
        label='Curso'
    )
    data_inscricao = forms.DateField(
        required=False,
        label='Data de Inscrição',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['curso'].queryset = Curso.objects.all()
        except:
            self.fields['curso'].queryset = Curso.objects.none()

# ---------------------------
# Formulário para Criar Aluno
# ---------------------------
class AlunoForm(forms.ModelForm):
    preferencia_turno = forms.ChoiceField(
        choices=PERIODO_CHOICES,
        widget=forms.RadioSelect,
        label='Turno preferido para entrevista'
    )

    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'curso', 'preferencia_turno']
        labels = {
            'nome': 'Nome do Aluno',
            'email': 'Email',
            'curso': 'Curso escolhido',
        }

# ---------------------------
# Formulário de Administrador
# ---------------------------
class CriarAdministradorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'senha']
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail'
        }

# ---------------------------
# Formulário de Agendamento
# ---------------------------
class AgendamentoForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label="Curso")
    quantidade_alunos = forms.IntegerField(min_value=1, label="Qtd. de alunos")
    periodo = forms.ChoiceField(
        choices=PERIODO_CHOICES,
        widget=forms.RadioSelect,
        label="Período"
    )
    dia_agendamento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data"
    )

# ---------------------------
# Formulário para editar Entrevistas
# ---------------------------
class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = ['aluno', 'curso', 'data_hora', 'local']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'aluno': 'Aluno',
            'curso': 'Curso',
            'data_hora': 'Data e Hora',
            'local': 'Local da Entrevista',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fields['data_hora'].initial:
            self.fields['data_hora'].initial = (
                timezone.now() + timedelta(hours=1)
            ).strftime('%Y-%m-%dT%H:%M')
