from django.contrib import admin
from .models import Agendamento, Passageiro

class PassageiroInline(admin.TabularInline):
    model  = Passageiro
    extra  = 1
    fields = ('nome', 'tipo', 'documento', 'telefone')

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo_servico', 'data_hora', 'veiculo', 'motorista', 'status', 'pagamento', 'valor_total')
    list_filter   = ('status', 'pagamento', 'tipo_servico')
    search_fields = ('cliente__nome', 'destino', 'codigo_voo')
    inlines       = [PassageiroInline]

@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'documento', 'agendamento')

    