from django.contrib import admin
from django.urls import path, include
from agendamentos import views as ag_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ag_views.dashboard, name='dashboard'),
    path('agendamentos/', include('agendamentos.urls', namespace='agendamentos')),
]