from django.contrib import admin
from .models import Perfil, Aluno, FormularioMarcacao, Curso, Entrevista

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'cpf', 'celular', 'score_vulnerabilidade')
    search_fields = ('user__username', 'nome', 'cpf', 'celular')
    list_filter = ('tipo', 'score_vulnerabilidade')
    ordering = ('-score_vulnerabilidade',)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'curso', 'data_inscricao', 'data_entrevista', 'score', 'preferencia_turno')
    search_fields = ('nome', 'email', 'curso__nome')
    list_filter = ('curso', 'data_entrevista', 'preferencia_turno')
    ordering = ('-data_inscricao',)
    readonly_fields = ('data_inscricao',)


@admin.register(FormularioMarcacao)
class FormularioMarcacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'score', 'data_envio')
    search_fields = ('usuario__username',)
    list_filter = ('score', 'data_envio')
    ordering = ('-data_envio',)


@admin.register(Entrevista)
class EntrevistaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_formatada', 'hora_formatada', 'local')
    list_filter = ('curso', 'data_hora')
    search_fields = ('aluno__nome', 'curso__nome')

    def data_formatada(self, obj):
        return obj.data_hora.strftime('%d/%m/%Y')
    data_formatada.short_description = "Data"

    def hora_formatada(self, obj):
        return obj.data_hora.strftime('%H:%M')
    hora_formatada.short_description = "Hora"


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)
