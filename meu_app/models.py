from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]
    turno = models.CharField(
        max_length=6,
        choices=TURNO_CHOICES,
        default='manha',
        verbose_name='Turno'
    )

    def __str__(self):
        return f"{self.nome} – {self.get_turno_display()}"

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
    curso = models.ForeignKey(
        Curso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Curso desejado"
    )

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, verbose_name="Curso escolhido")
    data_inscricao = models.DateTimeField(auto_now_add=True, editable=False)
    data_entrevista = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0)
    cpf = models.CharField(max_length=14, null=True, blank=True, verbose_name="CPF")
    
    PREFERENCIA_TURNO = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('indiferente', 'Indiferente'),
    ]
    preferencia_turno = models.CharField(
        max_length=12,
        choices=PREFERENCIA_TURNO,
        default='indiferente',
        verbose_name="Preferência de Entrevista"
    )

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

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]
    turno = models.CharField(
        max_length=10,
        choices=TURNO_CHOICES,
        null=True,
        blank=True
    )

    @property
    def curso_turno(self):
        if self.curso and self.turno:
            return f"{self.curso.nome} ({self.get_turno_display()})"
        return None

class Entrevista(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    local = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.aluno.nome} - {self.data_hora.strftime('%d/%m %H:%M')}"
