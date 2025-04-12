from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import re
from django.core.exceptions import ValidationError

def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")
    
    def calcular_digito(cpf, posicoes):
        soma = 0
        for i in range(posicoes):
            soma += int(cpf[i]) * (posicoes - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calcular_digito(cpf, 9)
    digito2 = calcular_digito(cpf, 10)

    if cpf[-2:] != f"{digito1}{digito2}":
        raise ValidationError("CPF inválido.")

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)  
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)

    def set_senha(self, senha):
        self.senha = make_password(senha)

    def verificar_senha(self, senha):
        return check_password(senha, self.senha)

    def __str__(self):
        return self.nome