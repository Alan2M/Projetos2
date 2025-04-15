from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")  
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)  

    def __str__(self):
        return self.user.username

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    serie = models.CharField(max_length=50)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome