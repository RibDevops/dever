from django.urls import path
from . import views

urlpatterns = [
    path('instancias/criar/', views.criar_instancia, name='criar-instancia'),
    path('instancias/', views.listar_instancias, name='listar-instancias'),
    path('instancias/<int:instance_id>/status/', 
         views.status_instancia, name='status-instancia'),
    path('mensagens/enviar/', views.enviar_mensagem, name='enviar-mensagem'),
]