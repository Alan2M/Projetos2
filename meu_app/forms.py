from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class CadastroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cpf', 'email']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Usuario.objects.filter(cpf=cpf).exists():
            raise ValidationError("Já existe um usuário cadastrado com esse CPF.")
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário cadastrado com esse E-mail.")
        return email
