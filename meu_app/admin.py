from django.contrib import admin
from .models import Perfil
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'celular', 'score_vulnerabilidade')
    search_fields = ('user__username', 'cpf', 'celular')
    list_filter = ('score_vulnerabilidade',)
    ordering = ('-score_vulnerabilidade',)

