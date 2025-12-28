from django.contrib import admin
from .models import Filme, Sessao, Ingresso

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracao_minutos', 'classificacao')
    search_fields = ('titulo',)

@admin.register(Sessao)
class SessaoAdmin(admin.ModelAdmin):
    list_display = ('filme', 'sala', 'horario')
    list_filter = ('sala', 'horario')

@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = ('id', 'sessao', 'data_venda', 'forma_pagamento')
    list_filter = ('data_venda', 'forma_pagamento')
