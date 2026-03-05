from django.shortcuts import render
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta
import json
from .models import Agendamento
from django.conf import settings


def agendamento_lista(request):
    qs = Agendamento.objects.select_related('cliente', 'veiculo', 'motorista').all()

    status = request.GET.get('status')
    tipo   = request.GET.get('tipo')
    q      = request.GET.get('q')

    if status:
        qs = qs.filter(status=status)
    if tipo:
        qs = qs.filter(tipo_servico=tipo)
    if q:
        qs = qs.filter(
            Q(cliente__nome__icontains=q) |
            Q(destino__icontains=q) |
            Q(codigo_voo__icontains=q)
        )

    return render(request, 'agendamentos/lista.html', {
        'agendamentos': qs,
        'status_choices': Agendamento.Status.choices,
        'tipo_choices': Agendamento.TipoServico.choices,
        'filtro_status': status,
        'filtro_tipo': tipo,
        'busca': q,
    })


def dashboard(request):
    hoje = timezone.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje)
    agendamentos_semana = Agendamento.objects.filter(data_hora__date__range=[inicio_semana, fim_semana])
    total_hoje = agendamentos_hoje.aggregate(t=Sum('valor_total'))['t'] or 0
    total_semana = agendamentos_semana.aggregate(t=Sum('valor_total'))['t'] or 0

    proximos = Agendamento.objects.select_related('cliente', 'veiculo', 'motorista').filter(
        data_hora__gte=timezone.now(),
        status__in=['pendente', 'confirmado']
    ).order_by('data_hora')[:5]

    labels = []
    valores = []
    for i in range(6, -1, -1):
        dia = hoje - timedelta(days=i)
        total = Agendamento.objects.filter(data_hora__date=dia).aggregate(t=Sum('valor_total'))['t'] or 0
        labels.append(dia.strftime('%d/%m'))
        valores.append(float(total))

    eventos = []
    for ag in Agendamento.objects.select_related('cliente').all():
        cor = {
            'pendente': '#f0c040',
            'confirmado': '#4caf50',
            'concluido': '#2196f3',
            'cancelado': '#e05a5a',
        }.get(ag.status, '#b8935a')
        eventos.append({
            'title': f'{ag.cliente.nome} — {ag.get_tipo_servico_display()}',
            'start': ag.data_hora.isoformat(),
            'color': cor,
        })

    return render(request, 'agendamentos/dashboard.html', {
        'agendamentos_hoje': agendamentos_hoje.count(),
        'agendamentos_semana': agendamentos_semana.count(),
        'total_hoje': total_hoje,
        'total_semana': total_semana,
        'proximos': proximos,
        'labels': json.dumps(labels),
        'valores': json.dumps(valores),
        'eventos': json.dumps(eventos),
    })

def os_motorista(request, pk):
    agendamento = Agendamento.objects.select_related(
        'cliente', 'veiculo', 'motorista', 'passeio'
    ).get(pk=pk)
    passageiros = agendamento.passageiros.all()
    return render(request, 'agendamentos/os_motorista.html', {
        'agendamento': agendamento,
        'passageiros': passageiros,
        'empresa': settings.EMPRESA,
    })


def orcamento_turista(request, pk):
    agendamento = Agendamento.objects.select_related(
        'cliente', 'veiculo', 'motorista', 'passeio'
    ).get(pk=pk)
    passageiros = agendamento.passageiros.all()
    return render(request, 'agendamentos/orcamento_turista.html', {
        'agendamento': agendamento,
        'passageiros': passageiros,
        'empresa': settings.EMPRESA,
    })

def agendamento_detalhe(request, pk):
    agendamento = Agendamento.objects.select_related(
        'cliente', 'veiculo', 'motorista', 'passeio'
    ).get(pk=pk)
    passageiros = agendamento.passageiros.all()
    return render(request, 'agendamentos/detalhe.html', {
        'agendamento': agendamento,
        'passageiros': passageiros,
        'empresa': settings.EMPRESA,
    })