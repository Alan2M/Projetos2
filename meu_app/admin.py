from django.contrib import admin
from .models import Perfil, Aluno, FormularioMarcacao

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'cpf', 'celular', 'score_vulnerabilidade')
    search_fields = ('user__username', 'nome', 'cpf', 'celular')
    list_filter = ('tipo', 'score_vulnerabilidade')
    ordering = ('-score_vulnerabilidade',)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'curso_escolhido', 'data_inscricao', 'data_entrevista')
    search_fields = ('nome', 'email', 'serie')
    list_filter = ('serie', 'data_entrevista')
    ordering = ('-data_inscricao',)

    def curso_escolhido(self, obj):
        return obj.serie
    curso_escolhido.short_description = "Curso escolhido"

@admin.register(FormularioMarcacao)
class FormularioMarcacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'score', 'data_envio')
    search_fields = ('usuario__username',)
    list_filter = ('score', 'data_envio')
    ordering = ('-data_envio',)
