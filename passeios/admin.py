from django.contrib import admin
from .models import Passeio

@admin.register(Passeio)
class PasseioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_horas', 'valor_onix', 'valor_spin', 'ativo')