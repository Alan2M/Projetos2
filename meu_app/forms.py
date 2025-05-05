from django import forms
from django.contrib.auth.models import User
from .models import Aluno
import datetime

class FiltroAlunoForm(forms.Form):
    nome = forms.CharField(required=False, label='Nome')
    email = forms.CharField(required=False, label='Email')
    cpf = forms.CharField(required=False, label='CPF')
    serie = forms.CharField(required=False, label='Curso')
    data_inscricao = forms.DateField(
        required=False, label='Data de Inscrição',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

# forms.py
class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'serie', 'data_entrevista']  # ❌ sem 'data_inscricao'
        labels = {
            'nome': 'Nome do Aluno',
            'email': 'Email',
            'serie': 'Curso escolhido',
            'data_entrevista': 'Data da entrevista',
        }
        widgets = {
            'data_entrevista': forms.DateInput(attrs={'type': 'date'}),
        }

class CriarAdministradorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'senha']
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail'
        }
