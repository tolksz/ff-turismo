from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('', views.agendamento_lista, name='lista'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/os-motorista/', views.os_motorista, name='os_motorista'),
    path('<int:pk>/orcamento-turista/', views.orcamento_turista, name='orcamento_turista'),
    path('<int:pk>/', views.agendamento_detalhe, name='detalhe'),
]