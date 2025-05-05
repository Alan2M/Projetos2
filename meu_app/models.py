from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    data_nascimento = models.DateField()
    score_vulnerabilidade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    serie = models.CharField("Curso escolhido", max_length=50)
    data_inscricao = models.DateTimeField(auto_now_add=True, editable=False)  # ✅ não editável
    data_entrevista = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

class FormularioMarcacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pessoas_moram = models.CharField(max_length=50)
    casa = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=50)
    escolaridade_pai = models.CharField(max_length=50)
    escolaridade_mae = models.CharField(max_length=50)
    renda_familiar = models.CharField(max_length=50)
    renda_mensal = models.CharField(max_length=50)
    trabalha = models.CharField(max_length=10)
    score = models.IntegerField(default=0)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - Score: {self.score}'
