from django.contrib import admin
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'placa', 'capacidade', 'ativo')
    list_filter  = ('ativo',)