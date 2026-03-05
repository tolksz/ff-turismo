import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from clientes.models import Cliente
from veiculos.models import Veiculo
from motoristas.models import Motorista
from passeios.models import Passeio
from agendamentos.models import Agendamento, Passageiro

hoje = timezone.now().replace(hour=7, minute=30, second=0, microsecond=0)

c1 = Cliente.objects.get_or_create(cpf='109.861.181-09', defaults=dict(nome='Shirley Mendes da Silva', telefone='(51) 99123-4567', email='shirley@email.com'))[0]
c2 = Cliente.objects.get_or_create(cpf='078.250.241-50', defaults=dict(nome='Carlos Eduardo Ferreira', telefone='(51) 98765-4321', email='carlos@email.com'))[0]
c3 = Cliente.objects.get_or_create(cpf='321.654.987-11', defaults=dict(nome='Ana Paula Rodrigues',     telefone='(54) 99876-5432', email='ana@email.com'))[0]

onix = Veiculo.objects.get_or_create(placa='ABC-1234', defaults=dict(modelo='Chevrolet Onix', capacidade=4, ativo=True))[0]
spin = Veiculo.objects.get_or_create(placa='DEF-5678', defaults=dict(modelo='Chevrolet Spin', capacidade=6, ativo=True))[0]

m1 = Motorista.objects.get_or_create(cnh='12345678901', defaults=dict(nome='João da Silva',  telefone='(51) 99111-2222', tipo='proprio',  ativo=True))[0]
m2 = Motorista.objects.get_or_create(cnh='98765432101', defaults=dict(nome='Pedro Oliveira', telefone='(51) 99333-4444', tipo='proprio',  ativo=True))[0]
m3 = Motorista.objects.get_or_create(cnh='11122233344', defaults=dict(nome='Marcos Freitas', telefone='(54) 99777-8888', tipo='parceiro', empresa='Turismo Serra Gaúcha', ativo=True))[0]

p1 = Passeio.objects.get_or_create(nome='City Tour Gramado & Canela', defaults=dict(duracao_horas=8, valor_onix=Decimal('280'), valor_spin=Decimal('300'), ativo=True))[0]

a1 = Agendamento.objects.create(
    cliente=c1, veiculo=spin, motorista=m1,
    tipo_servico='transfer_ida_volta', data_hora=hoje + timedelta(days=1),
    endereco_embarque='Aeroporto Salgado Filho — POA', destino='Hotel Serra Azul — Gramado',
    codigo_voo='LA3952', num_adultos=2, num_adolescentes=1, num_criancas=1,
    malas_despachadas=3, malas_mao=4, reboque=False,
    valor_total=Decimal('600'), valor_sinal=Decimal('120'),
    status='confirmado', pagamento='parcial',
    observacoes='Receptivo com placa de identificação.'
)
a2 = Agendamento.objects.create(
    cliente=c2, veiculo=onix, motorista=m2,
    tipo_servico='transfer_out', data_hora=hoje + timedelta(days=2),
    endereco_embarque='Hotel Laghetto — Gramado', destino='Aeroporto Salgado Filho — POA',
    codigo_voo='G31840', num_adultos=2, num_adolescentes=0, num_criancas=0,
    malas_despachadas=2, malas_mao=2, reboque=False,
    valor_total=Decimal('500'), valor_sinal=Decimal('100'),
    status='confirmado', pagamento='pago', observacoes=''
)
a3 = Agendamento.objects.create(
    cliente=c3, veiculo=spin, motorista=m1, passeio=p1,
    tipo_servico='city_tour', data_hora=hoje + timedelta(days=3),
    endereco_embarque='Hotel Casa da Montanha — Gramado', destino='Gramado & Canela',
    num_adultos=3, num_adolescentes=0, num_criancas=0,
    malas_despachadas=0, malas_mao=0, reboque=False,
    valor_total=Decimal('300'), valor_sinal=Decimal('60'),
    status='pendente', pagamento='pendente',
    observacoes='Grupo prefere iniciar pelo Parque Knorr.'
)

Passageiro.objects.create(agendamento=a1, nome='Shirley Mendes da Silva', tipo='adulto',      documento='109.861.181-09', telefone='(51) 99123-4567')
Passageiro.objects.create(agendamento=a1, nome='Carlos Mendes da Silva',  tipo='adulto',      documento='078.250.241-50')
Passageiro.objects.create(agendamento=a1, nome='Pedro Mendes da Silva',   tipo='adolescente', documento='921.361.091-20')
Passageiro.objects.create(agendamento=a1, nome='Ana Mendes da Silva',     tipo='crianca')

Passageiro.objects.create(agendamento=a2, nome='Carlos Eduardo Ferreira', tipo='adulto', documento='078.250.241-50', telefone='(51) 98765-4321')
Passageiro.objects.create(agendamento=a2, nome='Fernanda Ferreira',       tipo='adulto', documento='111.222.333-44')

Passageiro.objects.create(agendamento=a3, nome='Ana Paula Rodrigues', tipo='adulto', documento='321.654.987-11', telefone='(54) 99876-5432')
Passageiro.objects.create(agendamento=a3, nome='Bruno Rodrigues',     tipo='adulto', documento='321.654.987-22')
Passageiro.objects.create(agendamento=a3, nome='Carla Rodrigues',     tipo='adulto', documento='321.654.987-33')

print("✅ Banco populado! 3 clientes, 2 veículos, 3 motoristas, 1 passeio, 3 agendamentos, 9 passageiros.")