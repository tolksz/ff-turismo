from django.contrib import admin
from .models import Motorista

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'empresa', 'telefone', 'ativo')
    list_filter  = ('tipo', 'ativo')